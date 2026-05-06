import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

STRING_FIELDS = ["id", "name", "email", "phone", "linkedin", "telegram",
                 "category", "location", "raw_text"]
LIST_FIELDS = ["skills", "languages"]
NESTED_LIST_FIELDS = ["experience", "education"]   

EXPERIENCE_KEYS = {"company": str, "role": str, "duration": str}
EDUCATION_KEYS = {"school": str, "degree": str, "year": int}

def _clean_string(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _clean_list(value) -> list:
    if not isinstance(value, list):
        return []
    return [str(x).strip() for x in value if str(x).strip()]


def _clean_experience(entries) -> list:
    if not isinstance(entries, list):
        return []
    cleaned = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        cleaned.append({
            "company": _clean_string(entry.get("company", "Unknown Company")) or "Unknown Company",
            "role":    _clean_string(entry.get("role",    "Professional"))    or "Professional",
            "duration":_clean_string(entry.get("duration","1 year"))          or "1 year",
        })
    return cleaned


def _clean_education(entries) -> list:
    if not isinstance(entries, list):
        return []
    cleaned = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        try:
            year = int(entry.get("year", 2015))
        except (ValueError, TypeError):
            year = 2015
        cleaned.append({
            "school": _clean_string(entry.get("school", "Addis Ababa University")) or "Addis Ababa University",
            "degree": _clean_string(entry.get("degree", "B.Sc."))                  or "B.Sc.",
            "year":   year,
        })
    return cleaned

def clean_record(record: dict) -> dict:
    rec = dict(record)

    for field in STRING_FIELDS:
        rec[field] = _clean_string(rec.get(field))

    for field in LIST_FIELDS:
        rec[field] = _clean_list(rec.get(field, []))

    rec["experience"] = _clean_experience(rec.get("experience", []))
    rec["education"]  = _clean_education(rec.get("education", []))

    if not rec["id"]:
        import uuid
        rec["id"] = str(uuid.uuid4())
    if not rec["name"]:
        rec["name"] = "Unknown Candidate"
    if not rec["category"]:
        rec["category"] = "tech"
    if not rec["location"]:
        rec["location"] = "Addis Ababa"
    if not rec["languages"]:
        rec["languages"] = ["Amharic", "English"]
    if not rec["skills"]:
        rec["skills"] = ["Communication"]
    if not rec["experience"]:
        rec["experience"] = [{"company": "Unknown", "role": "Professional", "duration": "1 year"}]
    if not rec["education"]:
        rec["education"] = [{"school": "Addis Ababa University", "degree": "B.Sc.", "year": 2018}]

    return rec

def remove_duplicates(records: List[dict]) -> List[dict]:
    seen_ids = set()
    pass1 = []
    for rec in records:
        rid = rec.get("id", "")
        if rid not in seen_ids:
            seen_ids.add(rid)
            pass1.append(rec)

    before = len(records)
    after_pass1 = len(pass1)

    seen_fingerprints = set()
    pass2 = []
    for rec in pass1:
        name = rec.get("name", "").lower().strip()
        category = rec.get("category", "").lower().strip()
        raw_prefix = rec.get("raw_text", "")[:120].lower().strip()
        fp = (name, category, raw_prefix)
        if fp not in seen_fingerprints:
            seen_fingerprints.add(fp)
            pass2.append(rec)

    logger.info(
        "Deduplication: %d → %d (pass1) → %d (pass2) records",
        before, after_pass1, len(pass2)
    )
    return pass2

def clean_dataset(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logger.info("Starting dataset cleaning on %d records …", len(records))

    cleaned = []
    errors = 0
    for i, rec in enumerate(records):
        try:
            cleaned.append(clean_record(rec))
        except Exception as exc:
            errors += 1
            logger.warning("Cleaning failed for record %d: %s", i, exc)

    cleaned = remove_duplicates(cleaned)
    logger.info(
        "Cleaning complete — %d records retained, %d errors dropped.",
        len(cleaned), errors
    )
    return cleaned
