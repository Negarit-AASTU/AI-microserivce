from pydantic import BaseModel
from typing import List

class MatchRequest(BaseModel):
    resume_embedding: List[float]
    job_embedding: List[float]