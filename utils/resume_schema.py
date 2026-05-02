def build_resume_embedding_text(parsed):
    skills = " ".join(parsed.get("skills", []))

    experience = " ".join([
        exp.get("title", "") + " " + exp.get("company", "")
        for exp in parsed.get("experience", [])
    ])

    projects = " ".join([
        p.get("name", "")
        for p in parsed.get("projects", [])
    ])

    education = " ".join([
        e.get("degree", "") + " " + e.get("field", "")
        for e in parsed.get("education", [])
    ])

    return f"{skills} {experience} {projects} {education}"