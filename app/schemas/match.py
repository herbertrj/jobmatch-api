from pydantic import BaseModel


class CandidateMatchResult(BaseModel):
    candidate_id: int
    candidate_name: str
    score: int
    matched_skills: list[str]
    missing_skills: list[str]
    experience_ok: bool
