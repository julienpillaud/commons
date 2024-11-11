"""
Domain models represent the core business logic and rules of the application.
These models are completely independent of infrastructure concerns.

All repositories in the application must convert their infrastructure models
to these domain models before returning them to the application layer.
"""

import datetime
import uuid
from typing import Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, PositiveInt


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


Domain_T = TypeVar("Domain_T", bound=DomainModel)
Create_T_contra = TypeVar("Create_T_contra", bound=BaseModel, contravariant=True)
Update_T_contra = TypeVar("Update_T_contra", bound=BaseModel, contravariant=True)


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


class PaginationParams(BaseModel):
    page: PositiveInt = 1
    limit: PositiveInt = 100


class PaginatedItems(BaseModel, Generic[Domain_T]):
    total: PositiveInt
    limit: PositiveInt
    items: list[Domain_T]
