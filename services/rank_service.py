from fastapi import APIRouter
from core.embedding import cosine_similarity
from schemas.rank_schema import RankRequest

router = APIRouter()

@router.post("/rank-jobs")
async def rank_jobs(data: RankRequest):

    results = []

    for job in data.jobs:
        score = cosine_similarity(
            data.resume_embedding,
            job.embedding
        )

        results.append({
            "job_id": job.job_id,
            "score": score
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "ranked_jobs": results
    }