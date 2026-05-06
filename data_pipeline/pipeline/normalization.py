import uuid
import logging
from typing import List, Dict, Any

from pipeline.contacts import generate_all_contacts
from pipeline.localization import (
    generate_ethiopian_name,
    generate_location,
    generate_languages,
    generate_education_history,
)
from pipeline.reconstruction import generate_experience_history
from pipeline.config import SUPPORTED_CATEGORIES

import random

logger = logging.getLogger(__name__)

def _normalize_string(value, fallback: str = "") -> str:
    if value is None:
        return fallback
    result = str(value).strip()
    return result if result else fallback


def _normalize_list(value, fallback=None) -> list:
    if fallback is None:
        fallback = []
    if isinstance(value, list):
        cleaned = [str(x).strip() for x in value if str(x).strip()]
        return cleaned if cleaned else fallback
    return fallback


def _normalize_experience(entries: list, category: str) -> list:
    if not isinstance(entries, list) or len(entries) == 0:
        return generate_experience_history(category, n=random.randint(1, 2))

    normalized = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        company = _normalize_string(entry.get("company"), fallback="Unknown Company")
        role = _normalize_string(entry.get("role"), fallback="Professional")
        duration = _normalize_string(entry.get("duration"), fallback="1 year")
        normalized.append({"company": company, "role": role, "duration": duration})

    return normalized if normalized else generate_experience_history(category)


def _normalize_education(entries: list, category: str) -> list:
    if not isinstance(entries, list) or len(entries) == 0:
        return generate_education_history(category, n=1)

    normalized = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        school = _normalize_string(entry.get("school"), fallback="Addis Ababa University")
        degree = _normalize_string(entry.get("degree"), fallback="B.Sc.")

        try:
            year = int(entry.get("year", 2015))
        except (ValueError, TypeError):
            year = 2015
        normalized.append({"school": school, "degree": degree, "year": year})

    return normalized if normalized else generate_education_history(category)

def normalize_record(record: dict) -> Dict[str, Any]:
    category = _normalize_string(record.get("category"), fallback="tech")
    if category not in SUPPORTED_CATEGORIES:
        category = random.choice(SUPPORTED_CATEGORIES)

    name = _normalize_string(record.get("name"))
    if not name:
        name = generate_ethiopian_name()

    contacts = generate_all_contacts(name)

    skills = _normalize_list(
        record.get("skills", []),
        fallback=["Communication", "Problem Solving"]
    )

    experience = _normalize_experience(record.get("experience", []), category)
    education = _normalize_education(record.get("education", []), category)

    location = _normalize_string(record.get("location")) or generate_location()
    languages = _normalize_list(record.get("languages", []), fallback=["Amharic", "English"])

    raw_text = _normalize_string(record.get("raw_text"))
    if not raw_text:
        raw_text = (
            f"{name} — {category.title()} professional based in {location}. "
            f"Skills: {', '.join(skills[:5])}."
        )

    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": contacts["email"],
        "phone": contacts["phone"],
        "linkedin": contacts["linkedin"],
        "telegram": contacts["telegram"],
        "category": category,
        "skills": skills,
        "experience": experience,
        "education": education,
        "location": location,
        "languages": languages,
        "raw_text": raw_text,
    }

def normalize_dataset(records: List[dict]) -> List[Dict[str, Any]]:
    normalized = []
    errors = 0
    for i, record in enumerate(records):
        try:
            normalized.append(normalize_record(record))
        except Exception as exc:
            errors += 1
            logger.warning("Failed to normalize record %d: %s", i, exc)

    logger.info(
        "Normalization complete — %d records normalized, %d errors skipped.",
        len(normalized), errors
    )
    return normalized
