from abc import ABC, abstractmethod
from typing import Any, Generic

from faker import Faker
from sqlalchemy.orm import Session

from app.domain.models import Domain_T
from app.infrastructure.repositories.base import Model_T

faker = Faker()


class BaseDataFactory(ABC, Generic[Domain_T]):
    schema: type[Domain_T]

    def __init__(self) -> None:
        self.data: dict[str, Domain_T] = {}

    @abstractmethod
    def _fake_data(self, **kwargs: Any) -> dict[str, Any]: ...

    def create_one(self, **kwargs: Any) -> Domain_T:
        entity_data = self._fake_data(**kwargs)
        entity = self.schema.model_validate(entity_data)
        self.data[str(entity.id)] = entity
        return entity

    def create_many(self, count: int, /) -> list[Domain_T]:
        return [self.create_one() for _ in range(count)]


class BaseSQLAlchemyFactory(Generic[Domain_T, Model_T]):
    schema: type[Domain_T]
    model: type[Model_T]

    def __init__(
        self, session: Session, data_factory: BaseDataFactory[Domain_T]
    ) -> None:
        self.session = session
        self.data_factory = data_factory

    def create_one(self, **kwargs: Any) -> Domain_T:
        entity = self.data_factory.create_one(**kwargs)
        model = self._to_model(entity)
        self.session.add(model)
        self.session.commit()
        return entity

    def create_many(self, count: int, /) -> list[Domain_T]:
        return [self.create_one() for _ in range(count)]

    def _to_model(self, entity: Domain_T) -> Model_T:
        return self.model(**entity.model_dump())
