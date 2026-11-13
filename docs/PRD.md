# Product Requirements Document — NDPA Incident Response and Breach Reporting Toolkit
Version 0.1 | Windows development | Source: undergraduate project proposal

## Purpose and source boundary
Create a lightweight web application for Nigerian organizations, particularly SMEs, to document and manage cybersecurity incidents and support NDPA-related breach reporting. This document translates the submitted proposal into implementable requirements. Details not specified by the proposal are explicitly marked **design decisions** and require approval.

## Project objectives (from proposal)
1. Unified legal, operational, and technical incident-response framework.
2. Centralized historical incident repository including lessons learned and improvements.
3. Lightweight web application for logging, tracking, and decision support.
4. User acceptance testing.

## Workflow (from methodology)
Detection → Triage → Containment → Investigation → Reporting.

## Required deliverables (from expected outcomes)
- Incident Response Playbook
- Breach Notification Decision Tree
- Standardized Templates
- Tabletop Exercise Pack
- Digital Prototype (optional in original proposal; selected for this build)

## Functional requirements
- FR-01: Create incident with identifier, description, detection date/time, reporter, affected system and initial status.
- FR-02: Track incident through the five named workflow stages with timestamps and notes.
- FR-03: Record incident type, severity rationale, affected data categories, affected people estimate and uncertainties.
- FR-04: Record containment actions, owners, timestamps and outcomes.
- FR-05: Record investigation notes and evidence metadata; do not claim forensic-grade custody without implementing it.
- FR-06: Provide a **rule-based** notification decision tree with explicit unanswered questions and a human decision field.
- FR-07: Generate editable incident record and breach-notification draft templates; no automatic external submission.
- FR-08: Maintain a historical repository with search/filter and post-incident lessons learned.
- FR-09: Provide a response playbook organized by the five workflow stages.
- FR-10: Provide a tabletop exercise scenario and evaluation checklist using synthetic data.
- FR-11: Support UAT with a documented test checklist and observed results.

## Proposed application pages (design decisions)
Dashboard; Incident Register; New Incident; Incident Detail (five stages); Notification Assessment; Reports/Templates; Playbook; Tabletop Exercise; Lessons Learned.

## Minimal data model (design decisions)
Incident(id, title, description, detected_at, created_at, type, severity, stage, affected_system, personal_data_involved, affected_data_categories, affected_people_estimate); IncidentAction(id, incident_id, stage, action, owner, timestamp, outcome); Assessment(id, incident_id, answers_json, outcome, reviewer, reviewed_at, rule_version); Report(id, incident_id, report_type, draft_text, approved_at); Lesson(id, incident_id, root_cause, improvement, follow_up); AuditEvent(id, incident_id, event_type, actor, timestamp, details).

## Non-functional requirements
- Simple SME-oriented interface; responsive on standard Windows browsers.
- SQLite persistence, input validation, explicit error messages, basic authentication and access control if time permits.
- No real personal data in demonstrations; synthetic cases only.
- Preserve change history; distinguish unknown facts from confirmed facts.
- No AI runtime or model calls.

## Legal safeguards
The proposal describes a 72-hour notification period, but its generalized wording is **not sufficient** to implement a legal determination. Obtain and review primary NDPA/NDPC material before finalizing reportability criteria, clock triggers and notification recipients. Until then, the decision tree is a review aid and returns **Needs human/legal review**, not definitive compliance judgments. Do not label the prototype certified or legally compliant.

## Out of scope
Live SIEM/EDR integrations; automatic regulator submission; enterprise-grade forensic processing; AI/agent inference; production hosting; binding legal advice.

## MVP acceptance criteria
- Create an incident and reload it from SQLite.
- Advance an incident through all five stages, retaining notes and action history.
- Complete a decision-tree questionnaire, save answers and obtain a clearly qualified review outcome.
- Generate and edit an incident report draft.
- View prior incidents and add a lesson learned.
- Run a simulated scenario and complete a UAT checklist.

## Open decisions
Exact notification rules pending primary-law verification; whether to include user accounts in two-hour build; export format (HTML/print or PDF); deployment target after demonstration.

## Development environment
Windows, Visual Studio Code, and OpenCode with Beam Free as the coding assistant. This choice does not add any AI capability to the application.
