from pydantic import BaseModel


class CandidateMatchResult(BaseModel):
    candidate_id: int
    candidate_name: str
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    experience_ok: bool


class JobMatchResult(BaseModel):
    job_id: int
    job_title: str
    company: str
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    experience_ok: bool
