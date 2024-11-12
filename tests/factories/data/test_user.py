import datetime

from app.domain.constants import UserConstants
from app.factories.user import UserDataFactory


def test_user_data_factory_create_one(user_data_factory: UserDataFactory) -> None:
    user = user_data_factory.create_one()

    assert user.id
    assert user.username
    assert "@" in user.email
    assert UserConstants.MIN_LEVEL <= user.level <= UserConstants.MAX_LEVEL
    assert UserConstants.MIN_HEIGHT <= user.height <= UserConstants.MAX_HEIGHT
    assert isinstance(user.is_active, bool)
    assert user.birth_date
    assert user.posts == []

    # Check if user in factory data
    assert str(user.id) in user_data_factory.data


def test_user_data_factory_create_one_with_override(
    user_data_factory: UserDataFactory,
) -> None:
    custom_data = {
        "username": "custom_username",
        "email": "custom@example.com",
        "level": 42,
        "height": 175.5,
        "is_active": False,
        "birth_date": datetime.date(2020, 1, 1),
    }

    user = user_data_factory.create_one(**custom_data)

    assert user.id
    assert user.username == custom_data["username"]
    assert user.email == custom_data["email"]
    assert user.level == custom_data["level"]
    assert user.height == custom_data["height"]
    assert user.is_active == custom_data["is_active"]
    assert user.birth_date == custom_data["birth_date"]
    assert user.posts == []

    # Check if user in factory data
    assert str(user.id) in user_data_factory.data


def test_user_data_factory_create_many(user_data_factory: UserDataFactory) -> None:
    count = 3

    users = user_data_factory.create_many(count)

    assert len(users) == count
    assert len(user_data_factory.data) == count
