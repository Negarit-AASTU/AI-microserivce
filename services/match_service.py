from fastapi import APIRouter
from core.embedding import cosine_similarity
from schemas.match_schema import MatchRequest

router = APIRouter()

@router.post("/match")
async def match(data: MatchRequest):

    score = cosine_similarity(
        data.resume_embedding,
        data.job_embedding
    )

    return {
        "match_score": round(score, 4)
    }