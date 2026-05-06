"""
smoke_test.py
=============
Validates every pipeline module WITHOUT requiring real dataset files.
Generates 20 synthetic records end-to-end and saves them to smoke_output.json.

Run:
    python smoke_test.py
"""

import sys
import json

print("=" * 60)
print("  🧪  NEGARIT PIPELINE — SMOKE TEST")
print("=" * 60)

# ── 1. Config ──────────────────────────────────────────────────────────────
print("\n[1/7] Loading config …", end=" ")
from pipeline.config import (
    SUPPORTED_CATEGORIES, ETHIOPIAN_FIRST_NAMES, ETHIOPIAN_LAST_NAMES,
    SKILLS_BY_CATEGORY, ROLES_BY_CATEGORY, COMPANIES_BY_CATEGORY,
)
assert len(SUPPORTED_CATEGORIES) == 6, "Expected 6 categories"
assert len(ETHIOPIAN_FIRST_NAMES) > 0
assert len(ETHIOPIAN_LAST_NAMES) > 0
for cat in SUPPORTED_CATEGORIES:
    assert cat in SKILLS_BY_CATEGORY,   f"Missing skills for: {cat}"
    assert cat in ROLES_BY_CATEGORY,    f"Missing roles for: {cat}"
    assert cat in COMPANIES_BY_CATEGORY,f"Missing companies for: {cat}"
print("✅")

# ── 2. Localization ────────────────────────────────────────────────────────
print("[2/7] Localization …", end=" ")
from pipeline.localization import (
    generate_ethiopian_name, generate_location, generate_languages,
    generate_university, generate_company, generate_degree,
    generate_education_history,
)
name = generate_ethiopian_name()
assert len(name.split()) >= 2, f"Name too short: {name}"
loc  = generate_location()
assert isinstance(loc, str) and loc
langs = generate_languages()
assert isinstance(langs, list) and len(langs) >= 2
uni  = generate_university()
assert isinstance(uni, str) and uni
edu  = generate_education_history("tech", n=2)
assert len(edu) == 2
assert all(k in edu[0] for k in ("school", "degree", "year"))
print("✅")

# ── 3. Contacts ────────────────────────────────────────────────────────────
print("[3/7] Contacts …", end=" ")
from pipeline.contacts import (
    generate_phone, generate_email, generate_linkedin,
    generate_telegram, generate_all_contacts,
)
phone = generate_phone()
assert phone.startswith("+251") or phone.startswith("09") or phone.startswith("+")
email = generate_email("Dawit Bekele")
assert "@" in email and "." in email
linkedin = generate_linkedin("Rahel Haile")
assert linkedin.startswith("https://www.linkedin.com/in/")
telegram = generate_telegram("Meron Tesfaye")
assert telegram.startswith("@")
contacts = generate_all_contacts("Solomon Girma")
assert all(k in contacts for k in ("email", "phone", "linkedin", "telegram"))
print("✅")

# ── 4. Reconstruction ──────────────────────────────────────────────────────
print("[4/7] Reconstruction …", end=" ")
from pipeline.reconstruction import (
    infer_category, generate_experience_entry,
    generate_experience_history, reconstruct_record,
)
cat = infer_category("Software engineer skilled in Python Django REST APIs")
assert cat == "tech", f"Expected tech, got {cat}"
cat2 = infer_category("nurse patient care hospital emergency")
assert cat2 == "healthcare", f"Expected healthcare, got {cat2}"
exp = generate_experience_history("finance", n=2)
assert len(exp) == 2
assert all(k in exp[0] for k in ("company", "role", "duration"))

# Reconstruct a sparse record
sparse = {"name": "", "category": "IT", "skills": [], "experience": [], "education": [], "raw_text": ""}
rec = reconstruct_record(sparse)
assert rec["name"], "Name should be generated"
assert rec["category"] in SUPPORTED_CATEGORIES
assert isinstance(rec["experience"], list) and len(rec["experience"]) > 0
assert isinstance(rec["education"], list) and len(rec["education"]) > 0
print("✅")

# ── 5. Enrichment ──────────────────────────────────────────────────────────
print("[5/7] Enrichment …", end=" ")
from pipeline.enrichment import parse_raw_skills, enrich_skills, enrich_record
skills_raw = "Python, Django, [REST APIs]"
parsed = parse_raw_skills(skills_raw)
assert "Python" in parsed
enriched_skills = enrich_skills("tech", parsed)
assert len(enriched_skills) > len(parsed)
assert len(enriched_skills) <= 18  # MAX_SKILLS cap

rec_to_enrich = {**rec, "skills": parsed}
enriched_rec = enrich_record(rec_to_enrich)
assert isinstance(enriched_rec["skills"], list)
assert len(enriched_rec["skills"]) > 0
print("✅")

# ── 6. Normalization ───────────────────────────────────────────────────────
print("[6/7] Normalization …", end=" ")
from pipeline.normalization import normalize_record, normalize_dataset

FINAL_KEYS = {"id","name","email","phone","linkedin","telegram",
              "category","skills","experience","education",
              "location","languages","raw_text"}

normalized = normalize_record(enriched_rec)
missing = FINAL_KEYS - set(normalized.keys())
assert not missing, f"Missing keys: {missing}"
assert isinstance(normalized["skills"], list)
assert isinstance(normalized["experience"], list)
assert isinstance(normalized["education"], list)
assert isinstance(normalized["languages"], list)
assert normalized["id"]  # non-empty UUID

# Build 20 synthetic records end-to-end
import random
synthetic_inputs = []
for i in range(20):
    cat = random.choice(SUPPORTED_CATEGORIES)
    r = reconstruct_record({"name":"","category":cat,"skills":[],"experience":[],"education":[],"raw_text":""})
    r = enrich_record(r)
    synthetic_inputs.append(r)

final_records = normalize_dataset(synthetic_inputs)
assert len(final_records) == 20
print("✅")

# ── 7. Cleaning ────────────────────────────────────────────────────────────
print("[7/7] Cleaning …", end=" ")
from pipeline.cleaning import clean_record, clean_dataset

for rec in final_records:
    cleaned = clean_record(rec)
    for field in ["id","name","email","phone","linkedin","telegram","category","location","raw_text"]:
        assert isinstance(cleaned[field], str), f"{field} is not str"
    assert isinstance(cleaned["skills"], list)
    assert isinstance(cleaned["languages"], list)
    assert isinstance(cleaned["experience"], list)
    assert isinstance(cleaned["education"], list)
    for exp in cleaned["experience"]:
        assert all(k in exp for k in ("company","role","duration"))
    for edu in cleaned["education"]:
        assert all(k in edu for k in ("school","degree","year"))
        assert isinstance(edu["year"], int)

cleaned_dataset = clean_dataset(final_records)
assert len(cleaned_dataset) > 0
print("✅")

# ── Save output ────────────────────────────────────────────────────────────
with open("smoke_output.json", "w", encoding="utf-8") as f:
    json.dump(cleaned_dataset, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print(f"  ✅  ALL TESTS PASSED — {len(cleaned_dataset)} records written to smoke_output.json")
print("=" * 60 + "\n")

# Print one sample record
print("── Sample Record ──────────────────────────────────────────")
sample = cleaned_dataset[0]
print(f"  Name     : {sample['name']}")
print(f"  Category : {sample['category']}")
print(f"  Location : {sample['location']}")
print(f"  Email    : {sample['email']}")
print(f"  Phone    : {sample['phone']}")
print(f"  LinkedIn : {sample['linkedin']}")
print(f"  Telegram : {sample['telegram']}")
print(f"  Skills   : {', '.join(sample['skills'][:4])} …")
print(f"  Exp[0]   : {sample['experience'][0]['role']} @ {sample['experience'][0]['company']}")
print(f"  Edu[0]   : {sample['education'][0]['degree']}, {sample['education'][0]['school']}")
print(f"  Languages: {', '.join(sample['languages'])}")
print()
