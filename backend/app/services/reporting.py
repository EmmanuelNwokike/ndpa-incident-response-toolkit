from datetime import datetime


def build_incident_report(incident) -> str:
    actions = getattr(incident, "actions", []) or []
    assessments = getattr(incident, "assessments", []) or []
    lessons = getattr(incident, "lessons", []) or []

    missing = []
    if not incident.affected_data_categories:
        missing.append("affected data categories")
    if incident.affected_people_estimate is None:
        missing.append("affected people estimate")
    if not incident.severity:
        missing.append("severity classification")
    if not assessments:
        missing.append("notification assessment")

    lines = []
    lines.append("INCIDENT REPORT DRAFT (editable)")
    lines.append("=" * 40)
    lines.append(f"Incident ID: {incident.id}")
    lines.append(f"Title: {incident.title}")
    lines.append(f"Description: {incident.description}")
    lines.append(f"Detected at: {incident.detected_at}")
    lines.append(f"Created at: {incident.created_at}")
    lines.append(f"Reporter: {incident.reporter}")
    lines.append(f"Affected system: {incident.affected_system}")
    lines.append(f"Incident type: {incident.incident_type or 'Not recorded'}")
    lines.append(f"Severity: {incident.severity or 'Not recorded'}")
    lines.append(f"Current stage: {incident.stage}")
    lines.append(f"Personal data involved: {incident.personal_data_involved}")
    lines.append(f"Affected data categories: {', '.join(incident.affected_data_categories or []) or 'Not recorded'}")
    lines.append(f"Affected people estimate: {incident.affected_people_estimate if incident.affected_people_estimate is not None else 'Not recorded'}")
    lines.append("")
    lines.append("CONTAINMENT / ACTIONS:")
    if actions:
        for a in actions:
            lines.append(f"- [{a.stage}] {a.action} (owner: {a.owner or 'n/a'}, {a.timestamp}) outcome: {a.outcome or 'n/a'} remarks: {a.remarks or 'n/a'}")
    else:
        lines.append("- None recorded")
    lines.append("")
    lines.append("NOTIFICATION ASSESSMENT:")
    if assessments:
        last = assessments[-1]
        lines.append(f"- Outcome: {last.outcome} (rule version {last.rule_version})")
        lines.append(f"- Reviewer: {last.reviewer or 'not assigned'}")
        lines.append(f"- Answers: {last.answers_json}")
    else:
        lines.append("- Not completed")
    lines.append("")
    lines.append("LESSONS LEARNED:")
    if lessons:
        for l in lessons:
            lines.append(f"- Root cause: {l.root_cause or 'n/a'}; improvement: {l.improvement or 'n/a'}; follow-up: {l.follow_up or 'n/a'}")
    else:
        lines.append("- None recorded")
    lines.append("")
    if missing:
        lines.append("MISSING INFORMATION:")
        for m in missing:
            lines.append(f"- {m}")
    else:
        lines.append("MISSING INFORMATION: none identified from recorded case facts.")
    lines.append("")
    lines.append("NOTE: This is a draft for human review. It does not assert legal compliance or reportability.")
    return "\n".join(lines)

def build_breach_notification_draft(incident) -> str:
    actions = getattr(incident, "actions", []) or []
    assessments = getattr(incident, "assessments", []) or []
    lines = []
    lines.append("DRAFT BREACH NOTIFICATION (for human review only)")
    lines.append("=" * 50)
    lines.append("This is a draft. It is not submitted automatically and does not assert legal compliance.")
    lines.append("")
    lines.append(f"Incident ID: {incident.id}")
    lines.append(f"Title: {incident.title}")
    lines.append(f"Description: {incident.description}")
    lines.append(f"Detected at: {incident.detected_at}")
    lines.append(f"Affected system: {incident.affected_system}")
    lines.append(f"Personal data involved: {incident.personal_data_involved}")
    lines.append(f"Affected data categories: {', '.join(incident.affected_data_categories or []) or 'Not recorded'}")
    lines.append(f"Affected people estimate: {incident.affected_people_estimate if incident.affected_people_estimate is not None else 'Not recorded'}")
    lines.append(f"Severity: {incident.severity or 'Not recorded'}")
    lines.append("")
    lines.append("Containment actions taken:")
    if actions:
        for a in actions:
            lines.append(f"- [{a.stage}] {a.action} (owner: {a.owner or 'n/a'}) outcome: {a.outcome or 'n/a'} remarks: {a.remarks or 'n/a'}")
    else:
        lines.append("- None recorded")
    lines.append("")
    lines.append("Assessment outcome: " + (assessments[-1].outcome if assessments else "Not completed"))
    lines.append("")
    lines.append("MISSING INFORMATION (to be completed before any notification):")
    missing = []
    if not incident.affected_data_categories: missing.append("affected data categories")
    if incident.affected_people_estimate is None: missing.append("affected people estimate")
    if not incident.severity: missing.append("severity classification")
    if not assessments: missing.append("notification assessment")
    if not actions: missing.append("containment actions")
    if missing:
        for m in missing: lines.append(f"- {m}")
    else:
        lines.append("- none identified")
    lines.append("")
    lines.append("NOTE: All regulatory notifications remain drafts requiring human/legal review.")
    return "\n".join(lines)
