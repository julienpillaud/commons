import uuid
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_user_service
from app.api.schemas import PaginatedResponse, UserResponse
from app.application.dtos import UserCreate, UserUpdate
from app.application.services.user import UserService
from app.domain.models import PaginationParams

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=PaginatedResponse[UserResponse])
def get_users(
    pagination: Annotated[PaginationParams, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
) -> Any:
    return service.get_all(pagination=pagination)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: uuid.UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> Any:
    return service.get_by_id(user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> Any:
    return service.create(user_create)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: uuid.UUID,
    user_update: UserUpdate,
    service: Annotated[UserService, Depends(get_user_service)],
) -> Any:
    return service.update(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: uuid.UUID,
    service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    service.delete(user_id)
