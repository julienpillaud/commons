import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


class UserDomain(DomainModel):
    username: str
    email: str
    level: int
    height: float
    is_active: bool
    birth_date: datetime.date
    posts: list["PostDomain"] = Field(default_factory=list)


class UserMinimalDomain(DomainModel):
    username: str
    email: str


class PostDomain(DomainModel):
    title: str
    content: str
    author_id: uuid.UUID
    author: UserMinimalDomain | None = None
    tags: list[str] = Field(default_factory=list)
