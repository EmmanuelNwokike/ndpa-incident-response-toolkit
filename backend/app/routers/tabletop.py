from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas
from ..services.content import TABLETOP_SCENARIOS

router = APIRouter(prefix="/tabletop", tags=["tabletop"])


@router.get("/scenarios")
def get_scenarios():
    return TABLETOP_SCENARIOS


@router.post("/runs", response_model=schemas.TabletopRunOut, status_code=201)
def create_run(payload: schemas.TabletopRunCreate, db: Session = Depends(get_db)):
    run = models.TabletopRun(
        scenario_id=payload.scenario_id,
        incident_id=payload.incident_id,
        respondent=payload.respondent,
        responses_json=payload.responses,
        evaluation_json=payload.evaluation,
        completed_at=datetime.now(timezone.utc) if payload.completed else None,
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run


@router.get("/runs", response_model=List[schemas.TabletopRunOut])
def list_runs(db: Session = Depends(get_db)):
    return db.query(models.TabletopRun).order_by(models.TabletopRun.id.desc()).all()


@router.get("/runs/{run_id}", response_model=schemas.TabletopRunOut)
def get_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(models.TabletopRun).filter(models.TabletopRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run


@router.patch("/runs/{run_id}", response_model=schemas.TabletopRunOut)
def update_run(run_id: int, payload: schemas.TabletopRunCreate, db: Session = Depends(get_db)):
    run = db.query(models.TabletopRun).filter(models.TabletopRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    run.responses_json = payload.responses
    run.evaluation_json = payload.evaluation
    if payload.completed:
        run.completed_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(run)
    return run
