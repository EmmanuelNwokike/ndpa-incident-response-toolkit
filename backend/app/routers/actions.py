from fastapi import APIRouter
from ..services.actions import ACTIONS, STAGES

router = APIRouter(prefix="/actions", tags=["actions"])


@router.get("/definitions")
def get_definitions():
    return {"stages": STAGES, "actions": ACTIONS}
