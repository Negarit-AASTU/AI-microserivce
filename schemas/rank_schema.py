from pydantic import BaseModel
from typing import List

class JobItem(BaseModel):
    job_id: str
    embedding: List[float]

class RankRequest(BaseModel):
    resume_embedding: List[float]
    jobs: List[JobItem]