import re

def clean_text(text: str) -> str:
    text = text.lower()

    # remove emails
    text = re.sub(r'\S+@\S+', ' ', text)

    # remove phone numbers
    text = re.sub(r'\+?\d[\d\s\-]{7,}', ' ', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()