import random
import re
import string
from pipeline.config import EMAIL_PROVIDERS, INTERNATIONAL_PHONE_PREFIXES

def generate_ethiopian_phone() -> str:
    fmt = random.choice(["intl_9", "intl_7", "local"])
    suffix = "".join(random.choices(string.digits, k=8))

    if fmt == "intl_9":
        return f"+2519{suffix}"
    elif fmt == "intl_7":
        return f"+2517{suffix}"
    else:
        return f"09{suffix}"

def generate_international_phone() -> str:
    prefix = random.choice(INTERNATIONAL_PHONE_PREFIXES)
    length = random.randint(7, 10)
    digits = "".join(random.choices(string.digits, k=length))
    return f"{prefix}{digits}"

def generate_phone(ethiopian_probability: float = 0.75) -> str:
    if random.random() < ethiopian_probability:
        return generate_ethiopian_phone()
    return generate_international_phone()

def _slugify_name(name: str) -> str:
    parts = name.lower().split()
    parts = [re.sub(r"[^a-z0-9]", "", p) for p in parts if p]
    return ".".join(parts) if parts else "user"


def generate_email(name: str) -> str:
    provider = random.choice(EMAIL_PROVIDERS)
    parts = name.lower().split()
    first = re.sub(r"[^a-z0-9]", "", parts[0]) if parts else "user"
    last = re.sub(r"[^a-z0-9]", "", parts[-1]) if len(parts) > 1 else ""

    pattern = random.choice(["full", "numbered", "initial"])

    if pattern == "full" and last:
        local = f"{first}.{last}"
    elif pattern == "numbered" and last:
        num = random.randint(10, 99)
        local = f"{first}.{last}{num}"
    else:
        local = f"{first[0]}.{last}" if last else first

    return f"{local}@{provider}"

def generate_linkedin(name: str) -> str:
    parts = name.lower().split()
    slug_parts = [re.sub(r"[^a-z0-9]", "", p) for p in parts]
    slug = "-".join(p for p in slug_parts if p)
    suffix = random.randint(1000, 9999)
    return f"https://www.linkedin.com/in/{slug}-{suffix}"

def generate_telegram(name: str) -> str:
    parts = name.split()
    first = re.sub(r"[^a-zA-Z0-9]", "", parts[0]) if parts else "User"
    last = re.sub(r"[^a-zA-Z0-9]", "", parts[-1]) if len(parts) > 1 else ""
    digits = "".join(random.choices(string.digits, k=3))
    handle = f"{first.capitalize()}{last.capitalize()}{digits}"
    return f"@{handle}"

def generate_all_contacts(name: str) -> dict:
    return {
        "email": generate_email(name),
        "phone": generate_phone(),
        "linkedin": generate_linkedin(name),
        "telegram": generate_telegram(name),
    }
