import random
import logging
from pipeline.config import SKILLS_BY_CATEGORY, ROLES_BY_CATEGORY, SUPPORTED_CATEGORIES
from pipeline.loaders import _parse_list_field

logger = logging.getLogger(__name__)
MAX_SKILLS = 18
MIN_SKILLS_THRESHOLD = 3

def parse_raw_skills(raw_skills) -> list:
    parsed = _parse_list_field(raw_skills)
    return [str(s).strip() for s in parsed if str(s).strip()]

def enrich_skills(category: str, existing_skills: list) -> list:
    pool = SKILLS_BY_CATEGORY.get(category, SKILLS_BY_CATEGORY["tech"])

    if len(existing_skills) >= MIN_SKILLS_THRESHOLD:
        add_count = random.randint(2, 5)
    else:
        add_count = random.randint(6, 12)

    available = [s for s in pool if s not in existing_skills]
    additions = random.sample(available, min(add_count, len(available)))

    combined = existing_skills + additions
    seen = set()
    deduped = []
    for skill in combined:
        key = skill.lower()
        if key not in seen:
            seen.add(key)
            deduped.append(skill)

    return deduped[:MAX_SKILLS]

def assign_role(category: str) -> str:
    roles = ROLES_BY_CATEGORY.get(category, ROLES_BY_CATEGORY["tech"])
    return random.choice(roles)

def diversify_experience_roles(experience: list, category: str) -> list:
    updated = []
    for entry in experience:
        if not isinstance(entry, dict):
            continue
        role = str(entry.get("role", "")).strip()
        if not role:
            entry = dict(entry)
            entry["role"] = assign_role(category)
        updated.append(entry)
    return updated

def enrich_record(record: dict) -> dict:
    rec = dict(record)
    category = rec.get("category", "tech")

    if category not in SUPPORTED_CATEGORIES:
        category = random.choice(SUPPORTED_CATEGORIES)
        rec["category"] = category
        logger.debug("Unknown category replaced with: %s", category)

    raw_skills = rec.get("skills", [])
    existing = parse_raw_skills(raw_skills)

    rec["skills"] = enrich_skills(category, existing)

    experience = rec.get("experience", [])
    if isinstance(experience, list):
        rec["experience"] = diversify_experience_roles(experience, category)

    return rec
