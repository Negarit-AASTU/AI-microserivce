from fastapi import APIRouter, Form
from core.embedding import embed_text
from core.text_cleaner import clean_text

router = APIRouter()

@router.post("/job")
async def job_embedding(job_description: str = Form(...)):

    cleaned = clean_text(job_description)
    embedding = embed_text(cleaned)

    return {
        "cleaned_text": cleaned,
        "embedding": embedding.tolist()
    }