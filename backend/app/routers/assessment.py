from fastapi import APIRouter
from ..services.decision_tree import QUESTIONS, RULE_VERSION

router = APIRouter(prefix="/assessment", tags=["assessment"])


@router.get("/questions")
def get_questions():
    return {"questions": QUESTIONS, "rule_version": RULE_VERSION}
