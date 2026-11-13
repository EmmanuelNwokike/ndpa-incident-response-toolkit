from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas
from ..services.workflow import STAGES, can_transition
from ..services.decision_tree import evaluate, RULE_VERSION
from ..services.reporting import build_incident_report

router = APIRouter(prefix="/incidents", tags=["incidents"])


def _incident_or_404(db: Session, incident_id: int):
    inc = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return inc


@router.get("", response_model=List[schemas.IncidentOut])
def list_incidents(q: Optional[str] = None, stage: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Incident)
    if q:
        like = f"%{q}%"
        query = query.filter((models.Incident.title.ilike(like)) | (models.Incident.description.ilike(like)))
    if stage:
        query = query.filter(models.Incident.stage == stage)
    return query.order_by(models.Incident.id.desc()).all()


@router.post("", response_model=schemas.IncidentOut, status_code=201)
def create_incident(payload: schemas.IncidentCreate, db: Session = Depends(get_db)):
    if payload.stage not in STAGES:
        raise HTTPException(status_code=422, detail="Invalid stage")
    inc = models.Incident(
        title=payload.title,
        description=payload.description,
        detected_at=payload.detected_at,
        reporter=payload.reporter,
        affected_system=payload.affected_system,
        incident_type=payload.incident_type,
        severity=payload.severity,
        stage=payload.stage,
        personal_data_involved=payload.personal_data_involved,
        affected_data_categories=payload.affected_data_categories,
        affected_people_estimate=payload.affected_people_estimate,
    )
    db.add(inc)
    db.commit()
    db.refresh(inc)
    db.add(models.AuditEvent(incident_id=inc.id, event_type="incident_created", details="Incident created"))
    db.commit()
    return inc


@router.get("/{incident_id}", response_model=schemas.IncidentOut)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    return _incident_or_404(db, incident_id)


@router.patch("/{incident_id}", response_model=schemas.IncidentOut)
def update_incident(incident_id: int, payload: schemas.IncidentUpdate, db: Session = Depends(get_db)):
    inc = _incident_or_404(db, incident_id)
    if payload.stage is not None:
        if payload.stage not in STAGES:
            raise HTTPException(status_code=422, detail="Invalid stage")
        if not can_transition(inc.stage, payload.stage):
            raise HTTPException(status_code=409, detail="Invalid stage transition")
        if payload.stage != inc.stage:
            db.add(models.AuditEvent(incident_id=inc.id, event_type="stage_changed", details=f"{inc.stage} -> {payload.stage}"))
        inc.stage = payload.stage
    if payload.title is not None:
        inc.title = payload.title
    if payload.description is not None:
        inc.description = payload.description
    if payload.severity is not None:
        inc.severity = payload.severity
    if payload.personal_data_involved is not None:
        inc.personal_data_involved = payload.personal_data_involved
    if payload.affected_data_categories is not None:
        inc.affected_data_categories = payload.affected_data_categories
    if payload.affected_people_estimate is not None:
        inc.affected_people_estimate = payload.affected_people_estimate
    if payload.notes:
        db.add(models.IncidentAction(incident_id=inc.id, stage=inc.stage, action=f"Note: {payload.notes}", owner=None, outcome=None))
    db.commit()
    db.refresh(inc)
    return inc


@router.post("/{incident_id}/actions", response_model=schemas.IncidentActionOut, status_code=201)
def add_action(incident_id: int, payload: schemas.IncidentActionCreate, db: Session = Depends(get_db)):
    inc = _incident_or_404(db, incident_id)
    if payload.stage not in STAGES:
        raise HTTPException(status_code=422, detail="Invalid stage")
    from ..services.actions import validate
    if not validate(payload.stage, payload.action, payload.outcome or ""):
        raise HTTPException(status_code=422, detail="Invalid stage/action/outcome combination")
    # prevent future stages
    from ..services.workflow import STAGES as WSTAGES
    if WSTAGES.index(payload.stage) > WSTAGES.index(inc.stage):
        raise HTTPException(status_code=409, detail="Cannot record action against future stage")
    ts = payload.timestamp or datetime.now(timezone.utc)
    action = models.IncidentAction(
        incident_id=inc.id,
        stage=payload.stage,
        action=payload.action,
        owner=payload.owner,
        outcome=payload.outcome,
        remarks=payload.remarks,
        timestamp=ts,
    )
    db.add(action)
    db.add(models.AuditEvent(incident_id=inc.id, event_type="action_added", details=payload.action))
    db.commit()
    db.refresh(action)
    return action


@router.post("/{incident_id}/assessment", response_model=schemas.AssessmentOut, status_code=201)
def create_assessment(incident_id: int, payload: schemas.AssessmentCreate, db: Session = Depends(get_db)):
    inc = _incident_or_404(db, incident_id)
    result = evaluate(payload.answers)
    assessment = models.Assessment(
        incident_id=inc.id,
        answers_json=payload.answers,
        missing_questions=result["missing_questions"],
        outcome=result["outcome"],
        reviewer=payload.reviewer,
        rule_version=result["rule_version"],
    )
    db.add(assessment)
    db.add(models.AuditEvent(incident_id=inc.id, event_type="assessment_created", details=result["outcome"]))
    db.commit()
    db.refresh(assessment)
    return assessment


@router.get("/{incident_id}/report", response_model=schemas.ReportOut)
def get_report(incident_id: int, db: Session = Depends(get_db)):
    inc = _incident_or_404(db, incident_id)
    # generate draft, reuse latest report if exists? Always regenerate draft to reflect facts; save new.
    draft = build_incident_report(inc)
    report = models.Report(incident_id=inc.id, report_type="incident_report", draft_text=draft)
    db.add(report)
    db.add(models.AuditEvent(incident_id=inc.id, event_type="report_generated", details="draft"))
    db.commit()
    db.refresh(report)
    return report


@router.patch("/{incident_id}/report/{report_id}", response_model=schemas.ReportOut)
def update_report(incident_id: int, report_id: int, payload: schemas.ReportUpdate, db: Session = Depends(get_db)):
    _incident_or_404(db, incident_id)
    report = db.query(models.Report).filter(models.Report.id == report_id, models.Report.incident_id == incident_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.draft_text = payload.draft_text
    db.commit()
    db.refresh(report)
    return report


@router.post("/{incident_id}/lessons", response_model=schemas.LessonOut, status_code=201)
def add_lesson(incident_id: int, payload: schemas.LessonCreate, db: Session = Depends(get_db)):
    inc = _incident_or_404(db, incident_id)
    lesson = models.Lesson(
        incident_id=inc.id,
        root_cause=payload.root_cause,
        improvement=payload.improvement,
        follow_up=payload.follow_up,
    )
    db.add(lesson)
    db.add(models.AuditEvent(incident_id=inc.id, event_type="lesson_added", details="lesson recorded"))
    db.commit()
    db.refresh(lesson)
    return lesson


@router.get("/{incident_id}/lessons", response_model=List[schemas.LessonOut])
def list_lessons(incident_id: int, db: Session = Depends(get_db)):
    _incident_or_404(db, incident_id)
    return db.query(models.Lesson).filter(models.Lesson.incident_id == incident_id).all()


@router.post("/{incident_id}/evidence", response_model=schemas.EvidenceOut, status_code=201)
def add_evidence(incident_id: int, payload: schemas.EvidenceCreate, db: Session = Depends(get_db)):
    inc = _incident_or_404(db, incident_id)
    from datetime import datetime, timezone
    ts = payload.collected_at or datetime.now(timezone.utc)
    ev = models.Evidence(
        incident_id=inc.id,
        description=payload.description,
        source=payload.source,
        collected_at=ts,
        collected_by=payload.collected_by,
        notes=payload.notes,
    )
    db.add(ev)
    db.add(models.AuditEvent(incident_id=inc.id, event_type="evidence_added", details=payload.description))
    db.commit()
    db.refresh(ev)
    return ev


@router.get("/{incident_id}/evidence", response_model=List[schemas.EvidenceOut])
def list_evidence(incident_id: int, db: Session = Depends(get_db)):
    _incident_or_404(db, incident_id)
    return db.query(models.Evidence).filter(models.Evidence.incident_id == incident_id).all()


@router.get("/{incident_id}/notification-draft")
def get_notification_draft(incident_id: int, db: Session = Depends(get_db)):
    from ..services.reporting import build_breach_notification_draft
    inc = _incident_or_404(db, incident_id)
    return {"draft_text": build_breach_notification_draft(inc)}
