import uuid
from typing import Any

from app.domain.constants import UserConstants
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
            "level": faker.random_int(
                min=UserConstants.MIN_LEVEL, max=UserConstants.MAX_LEVEL
            ),
            "height": faker.pyfloat(
                min_value=UserConstants.MIN_HEIGHT + 10,  # to be updated in tests
                max_value=UserConstants.MAX_HEIGHT - 10,  # to be updated in tests
                right_digits=2,
            ),
            "is_active": faker.boolean(),
            "birth_date": faker.date_of_birth(),
        }


class UserSQLAlchemyFactory(BaseSQLAlchemyFactory[UserDomain, User]):
    schema = UserDomain
    model = User
