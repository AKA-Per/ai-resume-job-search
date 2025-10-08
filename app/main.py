from fastapi import FastAPI
from app.api import routes_auth, routes_job, routes_company

from app.models.database import Base, engine

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Matcher Platform", version="0.2.0")

# Routes
app.include_router(routes_auth.router, prefix="/auth", tags=["Auth"])
app.include_router(routes_company.router, prefix="/companies", tags=["Companies"])
app.include_router(routes_job.router, prefix="/jobs", tags=["Jobs"])

@app.get("/")
def root():
    return {"message": "Platform API is running 🚀"}
