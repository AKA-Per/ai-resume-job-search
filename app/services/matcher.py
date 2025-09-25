# app/services/matcher.py
import random

def match_resume_to_job(resume_text: str, job_text: str):
    """
    Placeholder AI logic — later we’ll replace this with embeddings + similarity.
    """
    score = round(random.uniform(0, 1), 2)  # mock similarity score
    explanation = "This is a placeholder. Real AI logic coming soon!"
    return score, explanation
