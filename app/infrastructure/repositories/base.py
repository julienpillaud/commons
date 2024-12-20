import uuid
from typing import Any, Generic, TypeVar

from sqlalchemy import Select, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.models import (
    Create_T_contra,
    Domain_T,
    DomainPagination,
    PaginationParams,
    Update_T_contra,
)
from app.domain.repository import AbstractRepository
from app.infrastructure.exceptions import (
    DatabaseError,
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from app.infrastructure.models import Base

Model_T = TypeVar("Model_T", bound=Base)


class SQLAlchemyRepositoryBase(
    AbstractRepository[Domain_T, Create_T_contra, Update_T_contra],
    Generic[
        Model_T,
        Domain_T,
        Create_T_contra,
        Update_T_contra,
    ],
):
    model: type[Model_T]

    def __init__(self, session: Session):
        self.session = session

    def get_all(
        self, pagination: PaginationParams | None = None, **kwargs: Any
    ) -> DomainPagination[Domain_T]:
        count_stmt = select(func.count()).select_from(self.model)
        total = self.session.scalar(count_stmt) or 0

        stmt = select(self.model)
        stmt = self._apply_pagination(stmt=stmt, pagination=pagination)
        stmt = self._apply_loading_options(stmt=stmt, **kwargs)

        results = self.session.scalars(stmt)
        items = [self._to_domain(result) for result in results]

        return DomainPagination(total=total, limit=len(items), items=items)

    def get_by_id(self, entity_id: uuid.UUID, /, **kwargs: Any) -> Domain_T:
        stmt = select(self.model).where(self.model.id == entity_id)
        stmt = self._apply_loading_options(stmt=stmt, **kwargs)
        if entity := self.session.scalar(stmt):
            return self._to_domain(entity)

        raise EntityNotFoundError(self.model.__name__, str(entity_id))

    def create(self, data: Create_T_contra, /) -> Domain_T:
        db_model = self.model(**data.model_dump())
        self.session.add(db_model)
        try:
            self.session.commit()
        except IntegrityError as err:
            if "unique" in str(err).lower():
                raise EntityAlreadyExistsError(self.model.__name__) from err
            raise DatabaseError("insert", str(err)) from err

        return self._to_domain(db_model)

    def update(self, entity_id: uuid.UUID, data: Update_T_contra, /) -> Domain_T:
        entity = self.session.get(self.model, entity_id)
        if not entity:
            raise EntityNotFoundError(self.model.__name__, str(entity_id))

        entity_data = data.model_dump(exclude_unset=True)
        for key, value in entity_data.items():
            setattr(entity, key, value)

        self.session.commit()
        return self._to_domain(entity)

    def delete(self, entity_id: uuid.UUID, /) -> None:
        entity = self.session.get(self.model, entity_id)
        if not entity:
            raise EntityNotFoundError(self.model.__name__, str(entity_id))

        self.session.delete(entity)
        self.session.commit()

    def _to_domain(self, model: Model_T, /) -> Domain_T:
        return self.schema.model_validate(model)

    def _apply_loading_options(
        self, stmt: Select[tuple[Model_T]]
    ) -> Select[tuple[Model_T]]:
        return stmt

    @staticmethod
    def _apply_pagination(
        stmt: Select[tuple[Model_T]],
        pagination: PaginationParams | None,
    ) -> Select[tuple[Model_T]]:
        if pagination is None:
            return stmt

        offset = (pagination.page - 1) * pagination.limit
        return stmt.offset(offset).limit(pagination.limit)
