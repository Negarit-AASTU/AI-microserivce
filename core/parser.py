from transformers import pipeline
import json

extractor = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_length=512
)

def build_prompt(text: str):
    return f"""
Extract structured resume JSON.

Return ONLY valid JSON.

Schema:
{{
  "personal": {{"name":"","email":"","phone":"","location":""}},
  "skills": [],
  "experience": [],
  "education": [],
  "projects": [],
  "certifications": [],
  "languages": [],
  "links": {{"github":"","linkedin":"","portfolio":""}},
  "total_experience_years": 0
}}

Resume:
{text[:2000]}
"""

def parse_resume(text: str):
    prompt = build_prompt(text)
    output = extractor(prompt)[0]["generated_text"]

    try:
        return json.loads(output)
    except:
        return {"error": "invalid_json", "raw": output}