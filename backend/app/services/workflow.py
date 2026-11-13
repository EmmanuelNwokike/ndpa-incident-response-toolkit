STAGES = ["Detection", "Triage", "Containment", "Investigation", "Reporting"]


def stage_index(stage: str) -> int:
    if stage not in STAGES:
        raise ValueError(f"Unknown stage: {stage}")
    return STAGES.index(stage)


def can_transition(current: str, new: str) -> bool:
    if new not in STAGES:
        return False
    return STAGES.index(new) >= STAGES.index(current)


def next_stage(current: str):
    idx = STAGES.index(current)
    if idx + 1 < len(STAGES):
        return STAGES[idx + 1]
    return None