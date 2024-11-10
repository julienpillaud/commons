import uuid
from typing import Protocol, TypeVar

from pydantic import BaseModel

from app.domain.models import DomainModel

Domain_T = TypeVar("Domain_T", bound=DomainModel)
Create_T_contra = TypeVar("Create_T_contra", bound=BaseModel, contravariant=True)
Update_T_contra = TypeVar("Update_T_contra", bound=BaseModel, contravariant=True)


class AbstractRepository(Protocol[Domain_T, Create_T_contra, Update_T_contra]):
    schema: type[Domain_T]

    def get_all(self) -> list[Domain_T]: ...

    def get_by_id(self, entity_id: uuid.UUID) -> Domain_T: ...

    def create(self, data: Create_T_contra) -> Domain_T: ...

    def update(self, entity_id: uuid.UUID, data: Update_T_contra) -> Domain_T: ...

    def delete(self, entity_id: uuid.UUID) -> None: ...
