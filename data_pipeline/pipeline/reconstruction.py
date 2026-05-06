import random
import logging
from pipeline.config import (
    ROLES_BY_CATEGORY,
    COMPANIES_BY_CATEGORY,
    SUPPORTED_CATEGORIES,
    CATEGORY_KEYWORDS,
    EXPERIENCE_DURATION_MIN,
    EXPERIENCE_DURATION_MAX,
)
from pipeline.localization import (
    generate_ethiopian_name,
    generate_location,
    generate_languages,
    generate_education_history,
    generate_company,
)

logger = logging.getLogger(__name__)

def infer_category(raw_text: str) -> str:
    text = raw_text.lower()
    scores = {cat: 0 for cat in SUPPORTED_CATEGORIES}

    for category, keywords in CATEGORY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[category] += 1

    best = max(scores, key=scores.get)
    if scores[best] == 0:
        best = random.choice(SUPPORTED_CATEGORIES)
        logger.debug("No keyword match found; assigned random category: %s", best)
    return best


def _normalize_category(raw_category: str, raw_text: str) -> str:
    raw = raw_category.lower().strip()

    if raw in SUPPORTED_CATEGORIES:
        return raw

    for cat in SUPPORTED_CATEGORIES:
        if cat in raw:
            return cat

    aliases = {
        "information technology": "tech", "it": "tech", "software": "tech",
        "data science": "tech", "engineering": "tech", "developer": "tech",
        "banking": "finance", "accounting": "finance", "economics": "finance",
        "business": "sales", "commerce": "sales", "retail": "sales",
        "medical": "healthcare", "health": "healthcare", "nursing": "healthcare",
        "teaching": "education", "academic": "education",
        "supply chain": "logistics", "transport": "logistics",
    }
    for alias, mapped in aliases.items():
        if alias in raw:
            return mapped

    return infer_category(raw_text)

def generate_experience_entry(category: str) -> dict:
    company = generate_company(category)
    role = random.choice(ROLES_BY_CATEGORY.get(category, ROLES_BY_CATEGORY["tech"]))
    years = random.randint(EXPERIENCE_DURATION_MIN, EXPERIENCE_DURATION_MAX)
    duration = f"{years} year{'s' if years > 1 else ''}"
    return {"company": company, "role": role, "duration": duration}

def generate_experience_history(category: str, n: int = None) -> list:
    count = n if n is not None else random.randint(1, 3)
    return [generate_experience_entry(category) for _ in range(count)]

def reconstruct_record(record: dict) -> dict:
    rec = dict(record)  

    raw_cat = str(rec.get("category", "")).strip()
    raw_text = str(rec.get("raw_text", "")).strip()
    rec["category"] = _normalize_category(raw_cat, raw_text)
    category = rec["category"]

    if not str(rec.get("name", "")).strip():
        rec["name"] = generate_ethiopian_name()

    rec["location"] = generate_location()
    rec["languages"] = generate_languages()

    exp = rec.get("experience", [])
    if not isinstance(exp, list) or len(exp) == 0:
        rec["experience"] = generate_experience_history(category)

    edu = rec.get("education", [])
    if not isinstance(edu, list) or len(edu) == 0:
        rec["education"] = generate_education_history(category, n=random.randint(1, 2))

    if not raw_text:
        name = rec["name"]
        role = rec["experience"][0]["role"] if rec["experience"] else category
        rec["raw_text"] = (
            f"{name} is a {role} with expertise in {category.title()}. "
            f"Based in {rec['location']}, fluent in {', '.join(rec['languages'])}."
        )

    return rec
