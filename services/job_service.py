from fastapi import APIRouter, Form
from core.embedding import embed_text

router = APIRouter()

@router.post("/job")
async def job_embedding(job_description: str = Form(...)):

    embedding = embed_text(job_description)

    return {
        "job_description": job_description,
        "embedding": embedding.tolist()
    }