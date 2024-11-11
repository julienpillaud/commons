import uuid
from typing import Any, Generic, Protocol, TypeVar

from pydantic import BaseModel, PositiveInt

from app.application.schemas import PaginationParams
from app.domain.models import DomainModel

Domain_T = TypeVar("Domain_T", bound=DomainModel)
Create_T_contra = TypeVar("Create_T_contra", bound=BaseModel, contravariant=True)
Update_T_contra = TypeVar("Update_T_contra", bound=BaseModel, contravariant=True)


class PaginatedItems(BaseModel, Generic[Domain_T]):
    total: PositiveInt
    limit: PositiveInt
    items: list[Domain_T]


class AbstractRepository(Protocol[Domain_T, Create_T_contra, Update_T_contra]):
    schema: type[Domain_T]

    def get_all(
        self,
        pagination: PaginationParams | None = None,
    ) -> PaginatedItems[Domain_T]: ...

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> Domain_T: ...

    def create(self, data: Create_T_contra, /) -> Domain_T: ...

    def update(self, entity_id: uuid.UUID, data: Update_T_contra, /) -> Domain_T: ...

    def delete(self, entity_id: uuid.UUID, /) -> None: ...
