def build_skill_gap_prompt(resume_text: str, job_text: str):
    return f"""
You are an expert technical recruiter.

Compare the resume and job description.

Return ONLY valid JSON:

{{
  "matching_skills": [],
  "missing_skills": [],
  "weak_areas": [],
  "recommendations": []
}}

RULES:
- Be strict but fair
- Infer skills even if not explicitly written
- Focus on technical + soft skills

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_text}
"""