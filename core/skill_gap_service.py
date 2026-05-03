from google import genai
from core.json_parser import extract_json
from core.skill_gap_prompt_builder import build_skill_gap_prompt
import os

client = genai.Client()


def generate_skill_gap(resume_text: str, job_text: str):
    prompt = build_skill_gap_prompt(resume_text, job_text)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return extract_json(response.text)