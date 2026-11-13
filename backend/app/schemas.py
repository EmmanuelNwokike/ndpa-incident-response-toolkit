INCIDENT_ROLES = [
    "System Administrator",
    "Incident Response Manager",
    "Security Analyst",
    "IT Support Officer",
    "Data Protection Officer (DPO)",
    "Compliance Officer",
]
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field

STAGES = ["Detection", "Triage", "Containment", "Investigation", "Reporting"]


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    detected_at: datetime
    reporter: str = Field(..., min_length=1, max_length=200)
    affected_system: str = Field(..., min_length=1, max_length=200)
    incident_type: Optional[str] = None
    severity: Optional[Literal["High", "Medium", "Low"]] = None
    personal_data_involved: bool = False
    affected_data_categories: List[str] = Field(default_factory=list)
    affected_people_estimate: Optional[int] = Field(default=None, ge=0)
    stage: str = "Detection"


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[Literal["High", "Medium", "Low"]] = None
    stage: Optional[str] = None
    personal_data_involved: Optional[bool] = None
    affected_data_categories: Optional[List[str]] = None
    affected_people_estimate: Optional[int] = None
    notes: Optional[str] = None


class IncidentActionCreate(BaseModel):
    stage: str
    action: str = Field(..., min_length=1)
    owner: Literal["System Administrator", "Incident Response Manager", "Security Analyst", "IT Support Officer", "Data Protection Officer (DPO)", "Compliance Officer"]
    outcome: str
    remarks: Optional[str] = Field(default=None, max_length=2000)
    timestamp: Optional[datetime] = None


class AssessmentCreate(BaseModel):
    answers: Dict[str, Any] = Field(default_factory=dict)
    reviewer: Optional[str] = None


class ReportUpdate(BaseModel):
    draft_text: str


class LessonCreate(BaseModel):
    root_cause: Optional[str] = None
    improvement: Optional[str] = None
    follow_up: Optional[str] = None


class IncidentActionOut(BaseModel):
    id: int
    incident_id: int
    stage: str
    action: str
    owner: Optional[str]
    timestamp: datetime
    outcome: Optional[str]
    remarks: Optional[str]

    class Config:
        from_attributes = True


class AssessmentOut(BaseModel):
    id: int
    incident_id: int
    answers_json: Dict[str, Any]
    missing_questions: List[str] = []
    outcome: str
    reviewer: Optional[str]
    reviewed_at: datetime
    rule_version: str

    class Config:
        from_attributes = True


class ReportOut(BaseModel):
    id: int
    incident_id: int
    report_type: str
    draft_text: str
    approved_at: Optional[datetime]

    class Config:
        from_attributes = True


class LessonOut(BaseModel):
    id: int
    incident_id: int
    root_cause: Optional[str]
    improvement: Optional[str]
    follow_up: Optional[str]

    class Config:
        from_attributes = True


class AuditEventOut(BaseModel):
    id: int
    incident_id: Optional[int]
    event_type: str
    actor: Optional[str]
    timestamp: datetime
    details: Optional[str]

    class Config:
        from_attributes = True


class EvidenceCreate(BaseModel):
    description: str = Field(..., min_length=1)
    source: Optional[str] = None
    collected_at: Optional[datetime] = None
    collected_by: Optional[str] = None
    notes: Optional[str] = None


class EvidenceOut(BaseModel):
    id: int
    incident_id: int
    description: str
    source: Optional[str]
    collected_at: datetime
    collected_by: Optional[str]
    notes: Optional[str]

    class Config:
        from_attributes = True


class TabletopRunCreate(BaseModel):
    scenario_id: str
    incident_id: Optional[int] = None
    respondent: Optional[str] = None
    responses: dict = Field(default_factory=dict)
    evaluation: dict = Field(default_factory=dict)
    completed: bool = False


class TabletopRunOut(BaseModel):
    id: int
    scenario_id: str
    incident_id: Optional[int]
    respondent: Optional[str]
    responses_json: dict
    evaluation_json: dict
    started_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True


class IncidentOut(BaseModel):
    id: int
    title: str
    description: str
    detected_at: datetime
    created_at: datetime
    reporter: str
    affected_system: str
    incident_type: Optional[str]
    severity: Optional[Literal["High", "Medium", "Low"]]
    stage: str
    personal_data_involved: bool
    affected_data_categories: List[str]
    affected_people_estimate: Optional[int]
    actions: List[IncidentActionOut] = []
    assessments: List[AssessmentOut] = []
    reports: List[ReportOut] = []
    lessons: List[LessonOut] = []
    audit_events: List[AuditEventOut] = []
    evidence: List[EvidenceOut] = []

    class Config:
        from_attributes = True