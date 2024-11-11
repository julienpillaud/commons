import datetime
import uuid
from typing import TypeVar

from pydantic import BaseModel

from app.domain.models import PaginationBase


class APIResponse(BaseModel):
    id: uuid.UUID


Response_T = TypeVar("Response_T", bound=APIResponse)


class UserResponse(APIResponse):
    username: str
    email: str
    level: int
    height: float
    is_active: bool
    birth_date: datetime.date
    posts: list["PostResponse"]


class PostResponse(APIResponse):
    title: str
    content: str
    author_id: uuid.UUID
    tags: list[str]


class PaginatedResponse(PaginationBase[Response_T]): ...
