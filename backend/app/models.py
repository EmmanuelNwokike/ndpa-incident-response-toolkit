from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .database import Base

STAGES = ["Detection", "Triage", "Containment", "Investigation", "Reporting"]


class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    detected_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    reporter = Column(String(200), nullable=False)
    affected_system = Column(String(200), nullable=False)
    incident_type = Column(String(100), nullable=True)
    severity = Column(String(50), nullable=True)
    stage = Column(String(50), default="Detection", nullable=False)
    personal_data_involved = Column(Boolean, default=False, nullable=False)
    affected_data_categories = Column(JSON, default=list)
    affected_people_estimate = Column(Integer, nullable=True)

    actions = relationship("IncidentAction", back_populates="incident", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="incident", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="incident", cascade="all, delete-orphan")
    lessons = relationship("Lesson", back_populates="incident", cascade="all, delete-orphan")
    audit_events = relationship("AuditEvent", back_populates="incident", cascade="all, delete-orphan")


class IncidentAction(Base):
    __tablename__ = "incident_actions"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    stage = Column(String(50), nullable=False)
    action = Column(Text, nullable=False)
    owner = Column(String(200), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    outcome = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)

    incident = relationship("Incident", back_populates="actions")


class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    answers_json = Column(JSON, default=dict)
    missing_questions = Column(JSON, default=list)
    outcome = Column(String(100), nullable=False)
    reviewer = Column(String(200), nullable=True)
    reviewed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    rule_version = Column(String(50), nullable=False)

    incident = relationship("Incident", back_populates="assessments")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    report_type = Column(String(100), nullable=False)
    draft_text = Column(Text, nullable=False)
    approved_at = Column(DateTime, nullable=True)

    incident = relationship("Incident", back_populates="reports")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    root_cause = Column(Text, nullable=True)
    improvement = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)

    incident = relationship("Incident", back_populates="lessons")




class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=False)
    description = Column(Text, nullable=False)
    source = Column(String(300), nullable=True)
    collected_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    collected_by = Column(String(200), nullable=True)
    notes = Column(Text, nullable=True)

    incident = relationship("Incident", backref="evidence")


class TabletopRun(Base):
    __tablename__ = "tabletop_runs"

    id = Column(Integer, primary_key=True, index=True)
    scenario_id = Column(String(100), nullable=False)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    respondent = Column(String(200), nullable=True)
    responses_json = Column(JSON, default=dict)
    evaluation_json = Column(JSON, default=dict)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    completed_at = Column(DateTime, nullable=True)

    incident = relationship("Incident", backref="tabletop_runs")

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    event_type = Column(String(100), nullable=False)
    actor = Column(String(200), nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    details = Column(Text, nullable=True)

    incident = relationship("Incident", back_populates="audit_events")