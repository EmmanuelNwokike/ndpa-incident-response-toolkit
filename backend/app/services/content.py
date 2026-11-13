PLAYBOOK = {
    "Detection": [
        "Identify and record the event: what happened, when detected, by whom.",
        "Preserve initial evidence metadata (logs references, timestamps) without altering systems.",
        "Notify the incident owner/manager.",
    ],
    "Triage": [
        "Classify incident type and severity rationale.",
        "Determine whether personal data is involved and affected categories.",
        "Estimate affected individuals and note uncertainties.",
    ],
    "Containment": [
        "Take containment actions (isolate affected systems, revoke access, block traffic).",
        "Record owner, timestamp and outcome for each action.",
        "Verify containment effectiveness.",
    ],
    "Investigation": [
        "Collect findings and evidence metadata (no forensic-grade custody claimed).",
        "Identify root cause and scope of impact.",
        "Document uncertainties and gaps.",
    ],
    "Reporting": [
        "Complete notification decision questionnaire (human/legal review).",
        "Generate and edit incident report draft.",
        "Record lessons learned and follow-ups.",
    ],
}

TABLETOP_SCENARIOS = [
    {
        "id": "scenario-1",
        "title": "Misdirected customer spreadsheet",
        "description": (
            "An employee at a fictional Nigerian SME sends a spreadsheet containing customer "
            "contact information to an unintended external recipient. Detection time, exposure, "
            "recipients, and any subsequent access are initially uncertain."
        ),
        "tasks": [
            "Register the event",
            "Classify it provisionally",
            "Document containment",
            "Investigate affected data and recipients",
            "Complete notification decision questions",
            "Draft a report",
            "Record lessons learned",
        ],
        "evaluation_checklist": [
            "Case registered without technical assistance",
            "Case found in incident register",
            "Moved through five workflow stages preserving notes",
            "Playbook used for next-action suggestion",
            "Uncertainty recorded in notification questionnaire",
            "Report draft generated and edited",
            "Lesson learned recorded and retrieved",
        ],
    }
]