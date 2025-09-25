from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import database, job, company
from app.models.schemas import JobCreate
from app.models.job import Job

router = APIRouter()

@router.post("/", response_model=dict)
def create_job(payload: JobCreate, db: Session = Depends(database.get_db)):
    # Check if company exists
    db_company = db.query(company.Company).filter(company.Company.id == payload.company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    new_job = Job(
        title=payload.title,
        description=payload.description,
        education=payload.education,
        company_id=payload.company_id
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return {"message": "Job created successfully", "job_id": new_job.id}


@router.get("/", response_model=List[dict])
def list_jobs(db: Session = Depends(database.get_db)):
    jobs = db.query(job.Job).all()
    return [
        {
            "id": j.id,
            "title": j.title,
            "description": j.description,
            "education": j.education,
            "company_id": j.company_id,
            "company_name": j.company.name if j.company else None
        }
        for j in jobs
    ]


@router.get("/{job_id}", response_model=dict)
def get_job(job_id: int, db: Session = Depends(database.get_db)):
    db_job = db.query(job.Job).filter(job.Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": db_job.id,
        "title": db_job.title,
        "description": db_job.description,
        "education": db_job.education,
        "company_id": db_job.company_id,
        "company_name": db_job.company.name if db_job.company else None
    }
