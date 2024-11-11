import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_post_service
from app.api.schemas import PaginatedResponse, PostResponse
from app.application.dtos import PostCreate, PostUpdate
from app.application.services.post import PostService
from app.domain.models import PaginationParams

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=PaginatedResponse[PostResponse])
def get_posts(
    pagination: Annotated[PaginationParams, Depends()],
    service: Annotated[PostService, Depends(get_post_service)],
) -> Any:
    return service.get_all(pagination=pagination)


@router.get("/{post_id}", response_model=PostResponse)
def get_post(
    post_id: uuid.UUID,
    service: Annotated[PostService, Depends(get_post_service)],
) -> Any:
    return service.get_by_id(post_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(
    post_create: PostCreate,
    service: Annotated[PostService, Depends(get_post_service)],
) -> Any:
    return service.create(post_create)


@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: uuid.UUID,
    post_update: PostUpdate,
    service: Annotated[PostService, Depends(get_post_service)],
) -> Any:
    return service.update(post_id, post_update)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: uuid.UUID,
    service: Annotated[PostService, Depends(get_post_service)],
) -> None:
    service.delete(post_id)
