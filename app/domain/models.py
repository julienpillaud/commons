"""
Domain models represent the core business logic and rules of the application.
These models are completely independent of infrastructure concerns.

All repositories in the application must convert their infrastructure models
to these domain models before returning them to the application layer.
"""

import datetime
import uuid
from typing import Annotated, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt, PositiveInt

from app.domain.constants import UserConstants


class DomainModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID


T = TypeVar("T")
Domain_T = TypeVar("Domain_T", bound=DomainModel)
Create_T_contra = TypeVar("Create_T_contra", bound=BaseModel, contravariant=True)
Update_T_contra = TypeVar("Update_T_contra", bound=BaseModel, contravariant=True)


class UserDomain(DomainModel):
    username: str
    email: str
    level: Annotated[int, Field(ge=UserConstants.MIN_LEVEL, le=UserConstants.MAX_LEVEL)]
    height: Annotated[
        float, Field(ge=UserConstants.MIN_HEIGHT, le=UserConstants.MAX_HEIGHT)
    ]
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


class PaginationBase(BaseModel, Generic[T]):
    total: NonNegativeInt
    limit: NonNegativeInt
    items: list[T]


class DomainPagination(PaginationBase[Domain_T]): ...
