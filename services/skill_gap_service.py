from fastapi import APIRouter
from pydantic import BaseModel
from core.skill_gap_service import generate_skill_gap

router = APIRouter()


class SkillGapRequest(BaseModel):
    resume_text: str
    job_description: str


@router.post("/skill-gap")
async def skill_gap(data: SkillGapRequest):

    result = generate_skill_gap(
        data.resume_text,
        data.job_description
    )

    return {
        "analysis": result
    }