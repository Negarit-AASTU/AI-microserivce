from fastapi import APIRouter
from pydantic import BaseModel
from core.mcq_service import generate_mcqs

router = APIRouter()

class MCQRequest(BaseModel):
    job_description: str
    num_questions: int = 10


@router.post("/generate-mcqs")
async def generate(data: MCQRequest):

    questions = generate_mcqs(
        data.job_description,
        data.num_questions
    )

    return {
        "questions": questions
    }