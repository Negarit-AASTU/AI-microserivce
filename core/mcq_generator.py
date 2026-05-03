from google import genai
from core.prompt_builder import build_mcq_prompt
import os

client = genai.Client()  # reads GEMINI_API_KEY automatically

def generate_raw_mcqs(job_text: str, num_questions: int = 10):
    prompt = build_mcq_prompt(job_text, num_questions)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text