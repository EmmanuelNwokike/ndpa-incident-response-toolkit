ACTIONS = {
    "Detection": {
        "Record initial incident report": ["Incident recorded", "Additional information required", "Duplicate report identified"],
        "Identify affected systems": ["Affected systems identified", "Partially identified", "Investigation required"],
        "Identify potentially affected data": ["Data categories identified", "Personal data potentially involved", "Exposure not confirmed"],
        "Preserve initial evidence": ["Evidence recorded", "Evidence unavailable", "Preservation pending"],
    },
    "Triage": {
        "Assess incident severity": ["High severity", "Medium severity", "Low severity", "Assessment incomplete"],
        "Determine incident scope": ["Scope confirmed", "Partially confirmed", "Scope unknown"],
        "Assess potential impact": ["Impact identified", "Further assessment required", "No impact identified at this stage"],
        "Escalate to responsible officer": ["Escalation completed", "Escalation pending", "Further information requested"],
    },
    "Containment": {
        "Isolate affected systems": ["Systems isolated", "Partially isolated", "Isolation unsuccessful"],
        "Disable compromised accounts": ["Accounts disabled", "No compromised accounts identified", "Action pending"],
        "Revoke compromised access": ["Access revoked", "Access review required", "Revocation unsuccessful"],
        "Prevent further data exposure": ["Exposure contained", "Containment partially effective", "Exposure potentially ongoing"],
    },
    "Investigation": {
        "Determine root cause": ["Root cause identified", "Root cause suspected", "Root cause undetermined"],
        "Review system and access logs": ["Logs reviewed", "Relevant evidence identified", "Logs unavailable"],
        "Assess affected personal data": ["Affected data identified", "Further verification required", "No personal data exposure confirmed"],
        "Document investigation findings": ["Findings documented", "Investigation ongoing", "Additional evidence required"],
    },
    "Reporting": {
        "Prepare incident report": ["Draft completed", "Draft incomplete", "Additional information required"],
        "Complete breach notification assessment": ["Assessment recorded - needs review", "Additional information required", "Review pending"],
        "Submit report for internal review": ["Submitted for review", "Revision requested", "Approval pending"],
        "Record lessons learned": ["Lessons documented", "Corrective actions identified", "Follow-up required"],
    },
}

STAGES = ["Detection", "Triage", "Containment", "Investigation", "Reporting"]


def actions_for_stage(stage):
    return list(ACTIONS.get(stage, {}).keys())


def outcomes_for(stage, action):
    return ACTIONS.get(stage, {}).get(action, [])


def validate(stage, action, outcome):
    if stage not in ACTIONS:
        return False
    if action not in ACTIONS[stage]:
        return False
    if outcome not in ACTIONS[stage][action]:
        return False
    return True
