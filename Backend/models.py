import os
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Define the Candidate class using Pydantic
class Candidate(BaseModel):
    name: str
    email: str
    nationality: str
    phone: str
    education: str
    years_of_experience: int
    specialization: str
    skills: list[str]
    DOB: str
    CVPath: str
    Photo: str
    PhotoBack: Optional[str] = Field(default='default-photo-back.jpg')

class User(BaseModel):
    username: str
    password: str
    _type: str
    access_token: str
    expires_at: datetime