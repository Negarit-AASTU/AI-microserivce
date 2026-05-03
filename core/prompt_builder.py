def build_mcq_prompt(job_text: str, num_questions: int = 5):
    return f"""
You are a strict interview question generator.

Generate EXACTLY {num_questions} multiple-choice questions.

RULES:
- 4 options per question (A, B, C, D)
- ONLY ONE correct answer
- No explanations
- No numbering
- STRICT format below

FORMAT:

Q: ...
A: ...
B: ...
C: ...
D: ...
ANSWER: A/B/C/D

JOB:
{job_text[:1500]}
"""