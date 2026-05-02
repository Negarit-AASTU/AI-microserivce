import io
import docx
from pdfminer.high_level import extract_text

def extract_pdf(file_bytes: bytes):
    with io.BytesIO(file_bytes) as f:
        return extract_text(f)

def extract_docx(file_bytes: bytes):
    with io.BytesIO(file_bytes) as f:
        doc = docx.Document(f)
        return "\n".join([p.text for p in doc.paragraphs])