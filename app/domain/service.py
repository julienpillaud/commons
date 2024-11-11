import uuid
from typing import Any, Generic

from app.domain.models import (
    Create_T_contra,
    Domain_T,
    PaginatedItems,
    PaginationParams,
    Update_T_contra,
)
from app.domain.repository import AbstractRepository


class AbstractService(Generic[Domain_T, Create_T_contra, Update_T_contra]):
    def __init__(
        self, repository: AbstractRepository[Domain_T, Create_T_contra, Update_T_contra]
    ) -> None:
        self.repository = repository

    def get_all(
        self,
        pagination: PaginationParams | None = None,
        **kwargs: Any,
    ) -> PaginatedItems[Domain_T]:
        return self.repository.get_all(pagination=pagination, **kwargs)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> Domain_T:
        return self.repository.get_by_id(entity_id, **kwargs)

    def create(self, data: Create_T_contra, /) -> Domain_T:
        return self.repository.create(data)

    def update(self, entity_id: uuid.UUID, data: Update_T_contra, /) -> Domain_T:
        return self.repository.update(entity_id, data)

    def delete(self, entity_id: uuid.UUID, /) -> None:
        self.repository.delete(entity_id)
