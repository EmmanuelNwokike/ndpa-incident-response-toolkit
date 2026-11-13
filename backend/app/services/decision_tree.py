RULE_VERSION = "0.1-unverified (primary NDPA/NDPC rules pending verification)"

QUESTIONS = [
    {
        "id": "incident_type",
        "text": "What type of incident occurred?",
        "explanation": "Describe the incident category (e.g. phishing, unauthorized disclosure, ransomware).",
        "required": True,
    },
    {
        "id": "personal_data_involved",
        "text": "Does the incident involve personal data?",
        "explanation": "Indicate whether any personal data of individuals is involved.",
        "required": True,
    },
    {
        "id": "affected_data_categories",
        "text": "Which data categories are affected (e.g. contact, financial, health)?",
        "explanation": "List the categories of personal data potentially exposed.",
        "required": True,
    },
    {
        "id": "affected_people_estimate",
        "text": "Estimated number of affected individuals (0 if none/unknown)?",
        "explanation": "Provide a best-effort estimate; use 0 only if none or unknown.",
        "required": True,
    },
    {
        "id": "unauthorized_access",
        "text": "Was there confirmed unauthorized access or exfiltration?",
        "explanation": "Confirm whether data was accessed or removed without authorization.",
        "required": True,
    },
    {
        "id": "contained",
        "text": "Is the incident contained?",
        "explanation": "Indicate whether containment actions have stopped further exposure.",
        "required": True,
    },
    {
        "id": "regulator_deadline_verified",
        "text": "Has the applicable regulator notification deadline been verified against primary law?",
        "explanation": "Confirm whether the regulator notification deadline has been verified from primary NDPA/NDPC sources.",
        "required": True,
    },
]

REQUIRED_FACTS = [q["id"] for q in QUESTIONS if q["required"]]


def evaluate(answers: dict) -> dict:
    missing = []
    for q in QUESTIONS:
        val = answers.get(q["id"], None)
        if val is None or val == "" or val == "unknown" or val == "Unknown":
            if q["required"]:
                missing.append(q["id"])

    # Rule-based, non-definitive: never declare reportable/non-reportable.
    if missing:
        outcome = "Needs review"
        summary = (
            "Required facts are missing or unverified. This assessment is a review aid only; "
            "it does not determine legal reportability."
        )
    else:
        outcome = "Needs review"
        summary = (
            "All listed facts were provided, but legal reportability cannot be determined "
            "automatically. Human/legal review is required; deadline calculations remain disabled "
            "until primary NDPA/NDPC rules are verified."
        )

    return {
        "outcome": outcome,
        "missing_questions": missing,
        "summary": summary,
        "rule_version": RULE_VERSION,
        "human_decision_required": True,
    }