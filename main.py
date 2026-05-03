from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from services.resume_service import router as resume_router
from services.job_service import router as job_router
from services.match_service import router as match_router
from services.rank_service import router as rank_router
from services.question_service import router as question_router


app = FastAPI()

app.include_router(resume_router)
app.include_router(job_router)
app.include_router(match_router)
app.include_router(rank_router)
app.include_router(question_router)