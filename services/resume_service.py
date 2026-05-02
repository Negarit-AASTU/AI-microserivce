from fastapi import APIRouter, UploadFile, File
from core.extractor import extract_pdf, extract_docx
from core.parser import parse_resume
from core.embedding import embed_text
from utils.resume_schema import build_resume_embedding_text

router = APIRouter()

@router.post("/resume")
async def upload_resume(file: UploadFile = File(...)):
    content = await file.read()

    # 1. extract text
    if file.filename.endswith(".pdf"):
        text = extract_pdf(content)
    else:
        text = extract_docx(content)

    # 2. parse structured resume
    parsed = parse_resume(text)

    # 3. build embedding input
    embedding_input = build_resume_embedding_text(parsed)

    # 4. generate embedding
    embedding = embed_text(embedding_input)

    return {
        "parsed_resume": parsed,
        "embedding": embedding.tolist()
    }