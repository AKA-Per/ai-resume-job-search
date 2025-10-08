from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models import database, company
from app.models.company import Company
from app.models.schemas import CompanyCreate

from app.deps.auth import require_company

router = APIRouter()


@router.post("/", response_model=dict)
def create_company(payload: CompanyCreate, db: Session = Depends(database.get_db), current_user = Depends(require_company)):
    existing = db.query(Company).filter(Company.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company already exists")

    new_company = Company(
        name=payload.name,
        user_id=current_user.id,
        description=payload.description,
        website=payload.website
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return {"message": "Company created successfully", "company_id": new_company.id}


@router.get("/", response_model=List[dict])
def list_companies(db: Session = Depends(database.get_db), curren_user = Depends(require_company)):
    companies = db.query(Company).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "website": c.website
        }
        for c in companies
    ]


@router.get("/{company_id}", response_model=dict)
def get_company(company_id: int, db: Session = Depends(database.get_db), curren_user = Depends(require_company)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return {
        "id": db_company.id,
        "name": db_company.name,
        "description": db_company.description,
        "website": db_company.website,
    }


@router.put("/{company_id}", response_model=dict)
def update_company(company_id: int, payload: CompanyCreate, db: Session = Depends(database.get_db), curren_user = Depends(require_company)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    db_company.name = payload.name
    db_company.description = payload.description
    db_company.website = payload.website

    db.commit()
    db.refresh(db_company)
    return {"message": "Company updated successfully", "company_id": db_company.id}
