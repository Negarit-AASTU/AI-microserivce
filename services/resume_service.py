from fastapi import APIRouter, UploadFile, File
from core.extractor import extract_pdf, extract_docx
from core.embedding import embed_text
from core.text_cleaner import clean_text

router = APIRouter()

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()

    # 1. extract text
    if file.filename.endswith(".pdf"):
        text = extract_pdf(content)
    else:
        text = extract_docx(content)

    # 2. clean raw text
    cleaned = clean_text(text)

    # 4. generate embedding
    embedding = embed_text(cleaned)

    return {
        "text_preview": cleaned[:500],
        "embedding": embedding.tolist()
    }