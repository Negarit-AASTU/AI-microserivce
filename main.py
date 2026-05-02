from fastapi import FastAPI
from services.resume_service import router as resume_router
from services.job_service import router as job_router

app = FastAPI()

app.include_router(resume_router)
app.include_router(job_router)