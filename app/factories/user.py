import uuid
from typing import Any

from app.domain.models import UserDomain
from app.factories.base import BaseDataFactory, BaseSQLAlchemyFactory, faker
from app.infrastructure.models import User


class UserDataFactory(BaseDataFactory[UserDomain]):
    schema = UserDomain

    def _fake_data(self) -> dict[str, Any]:
        return {
            "id": uuid.uuid4(),
            "username": faker.unique.user_name(),
            "email": faker.unique.email(),
            "level": faker.random_int(min=1, max=100),
            "height": faker.pyfloat(min_value=100, max_value=200, right_digits=2),
            "is_active": faker.boolean(),
            "birth_date": faker.date_of_birth(minimum_age=18, maximum_age=90),
        }


class UserSQLAlchemyFactory(BaseSQLAlchemyFactory[UserDomain, User]):
    schema = UserDomain
    model = User
