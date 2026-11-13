from fastapi import APIRouter
from ..services.content import PLAYBOOK

router = APIRouter(prefix="/playbook", tags=["playbook"])


@router.get("")
def get_playbook():
    return PLAYBOOK