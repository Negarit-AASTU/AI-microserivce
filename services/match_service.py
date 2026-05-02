from fastapi import APIRouter
from core.embedding import cosine_similarity

router = APIRouter()

@router.post("/match")
async def match(resume_embedding: list, job_embedding: list):

    score = cosine_similarity(resume_embedding, job_embedding)

    return {
        "match_score": round(score, 4)
    }