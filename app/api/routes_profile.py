from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import profile as models
from app.models import user as user_model
from app.models import database
from app.schemas import profile as schemas
from app.deps.auth import require_candidate 

router = APIRouter()


# -------- PROFILE CRUD --------
@router.post("/", response_model=schemas.ProfileOut)
def create_or_update_profile(
    payload: schemas.ProfileCreate,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if db_profile:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_profile, key, value)
    else:
        db_profile = models.Profile(**payload.model_dump(), user_id=current_user.id)
        db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


@router.get("/", response_model=schemas.ProfileOut)
def get_profile(
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    db_profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return db_profile


# -------- EDUCATION CRUD --------
@router.post("/education/", response_model=schemas.EducationOut)
def add_education(
    payload: schemas.EducationCreate,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    edu = models.Education(**payload.model_dump(), profile_id=profile.id)
    db.add(edu)
    db.commit()
    db.refresh(edu)
    return edu


@router.delete("/education/{edu_id}", status_code=204)
def delete_education(
    edu_id: int,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    edu = db.query(models.Education).filter(models.Education.id == edu_id, models.Education.profile_id == profile.id).first()
    if not edu:
        raise HTTPException(status_code=404, detail="Education not found")
    db.delete(edu)
    db.commit()
    return


# -------- EXPERIENCE CRUD --------
@router.post("/experience/", response_model=schemas.ExperienceOut)
def add_experience(
    payload: schemas.ExperienceCreate,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    exp = models.Experience(**payload.dict(), profile_id=profile.id)
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/experience/{exp_id}", status_code=204)
def delete_experience(
    exp_id: int,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    exp = db.query(models.Experience).filter(models.Experience.id == exp_id, models.Experience.profile_id == profile.id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(exp)
    db.commit()
    return


# -------- SKILL CRUD --------
@router.post("/skill/", response_model=schemas.SkillOut)
def add_skill(
    payload: schemas.SkillCreate,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    skill = models.Skill(**payload.dict(), profile_id=profile.id)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


@router.delete("/skill/{skill_id}", status_code=204)
def delete_skill(
    skill_id: int,
    db: Session = Depends(database.get_db),
    current_user: user_model.User = Depends(require_candidate)
):
    profile = db.query(models.Profile).filter(models.Profile.user_id == current_user.id).first()
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id, models.Skill.profile_id == profile.id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    db.delete(skill)
    db.commit()
    return
