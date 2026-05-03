from core.mcq_generator import generate_raw_mcqs
from core.mcq_parser import parse_mcqs
from core.mcq_validator import validate_mcq

def generate_mcqs(job_text: str, num_questions: int = 5):

    raw_output = generate_raw_mcqs(job_text, num_questions)

    parsed = parse_mcqs(raw_output)

    valid_mcqs = [q for q in parsed if validate_mcq(q)]

    return valid_mcqs