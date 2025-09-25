# app/api/routes.py
from fastapi import APIRouter
from app.models.schemas import ResumeRequest, JobDescriptionRequest, MatchResponse
from app.services.matcher import match_resume_to_job

router = APIRouter()

@router.post("/match", response_model=MatchResponse)
async def match_resume(request: ResumeRequest, job: JobDescriptionRequest):
    """
    Takes resume text and job description, returns a match score and insights.
    """
    score, explanation = match_resume_to_job(request.text, job.text)
    return MatchResponse(score=score, explanation=explanation)
