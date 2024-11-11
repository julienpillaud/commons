import datetime
import uuid

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str
    email: str
    level: int = 0
    height: float
    is_active: bool = True
    birth_date: datetime.date


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    height: float | None = None


class PostCreate(BaseModel):
    title: str
    content: str
    author_id: uuid.UUID
    tags: list[str] = Field(default_factory=list)


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
