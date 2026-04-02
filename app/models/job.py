from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    company: Mapped[str] = mapped_column(String(120), nullable=False)
    minimum_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    required_skills_text: Mapped[str] = mapped_column(String, default="", nullable=False)
