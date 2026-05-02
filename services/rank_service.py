from fastapi import APIRouter

from core.embedding import cosine_similarity

router = APIRouter()

@router.post("/rank-jobs")
async def rank_jobs(data: dict):

    resume_embedding = data["resume_embedding"]
    jobs = data["jobs"]

    results = []

    for job in jobs:
        score = cosine_similarity(resume_embedding, job["embedding"])

        results.append({
            "job_id": job["job_id"],
            "score": score
        })

    # sort highest match first
    results.sort(key=lambda x: x["score"], reverse=True)

    return {
        "ranked_jobs": results
    }