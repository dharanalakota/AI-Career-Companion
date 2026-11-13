from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class ResumeData(BaseModel):

    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)


class ProfileCreate(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    education: str | None = Field(default=None, max_length=300)
    target_role: str | None = Field(default=None, max_length=120)


class ProfileResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    education: str | None = None
    target_role: str | None = None
    created_at: datetime
    resume_filename: str | None = None
    parsed_resume: ResumeData | None = None