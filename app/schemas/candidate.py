from pydantic import BaseModel, EmailStr, Field


class CandidateCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    email: EmailStr
    years_of_experience: int = Field(ge=0, le=50)
    skills: list[str] = Field(default_factory=list)


class CandidateResponse(CandidateCreate):
    id: int
