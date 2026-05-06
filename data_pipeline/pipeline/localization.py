import random
from pipeline.config import (
    ETHIOPIAN_FIRST_NAMES,
    ETHIOPIAN_LAST_NAMES,
    ETHIOPIAN_UNIVERSITIES,
    ETHIOPIAN_LOCATIONS,
    LANGUAGE_OPTIONS,
    COMPANIES_BY_CATEGORY,
    DEGREE_TYPES,
    SUPPORTED_CATEGORIES,
    GRADUATION_YEAR_MIN,
    GRADUATION_YEAR_MAX,
)

def generate_ethiopian_name() -> str:
    first = random.choice(ETHIOPIAN_FIRST_NAMES)
    last = random.choice(ETHIOPIAN_LAST_NAMES)
    return f"{first} {last}"

def generate_location() -> str:
    return random.choice(ETHIOPIAN_LOCATIONS)

def generate_languages() -> list:
    return list(random.choice(LANGUAGE_OPTIONS))

def generate_university() -> str:
    return random.choice(ETHIOPIAN_UNIVERSITIES)

def generate_company(category: str) -> str:
    companies = COMPANIES_BY_CATEGORY.get(
        category,
        COMPANIES_BY_CATEGORY[random.choice(SUPPORTED_CATEGORIES)]
    )
    return random.choice(companies)

def generate_degree(category: str) -> str:
    degrees = DEGREE_TYPES.get(category, DEGREE_TYPES["tech"])
    return random.choice(degrees)

def generate_graduation_year() -> int:
    return random.randint(GRADUATION_YEAR_MIN, GRADUATION_YEAR_MAX)

def generate_education_entry(category: str) -> dict:
    return {
        "school": generate_university(),
        "degree": generate_degree(category),
        "year": generate_graduation_year(),
    }

def generate_education_history(category: str, n: int = 1) -> list:
    return [generate_education_entry(category) for _ in range(n)]
