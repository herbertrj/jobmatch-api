from pydantic import BaseModel, Field


class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    company: str = Field(min_length=2, max_length=120)
    minimum_experience: int = Field(ge=0, le=50)
    required_skills: list[str] = Field(default_factory=list)


class JobResponse(JobCreate):
    id: int
