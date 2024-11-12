import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.factories.user import UserSQLAlchemyFactory
from app.infrastructure.models import User


def test_user_sqlalchemy_factory_create_one(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
) -> None:
    user = user_sqlalchemy_factory.create_one()
    user_db = session.get(User, user.id)

    assert user_db
    assert user_db.id == user.id
    assert user_db.username == user.username
    assert user_db.email == user.email
    assert user_db.level == user.level
    assert user_db.height == user.height
    assert user_db.is_active == user.is_active
    assert user_db.birth_date == user.birth_date


def test_user_sqlalchemy_factory_create_one_with_override(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
) -> None:
    custom_data = {
        "username": "custom_username",
        "email": "custom@example.com",
        "level": 42,
        "height": 175.5,
        "is_active": False,
        "birth_date": datetime.date(2020, 1, 1),
    }

    user = user_sqlalchemy_factory.create_one(**custom_data)
    user_db = session.get(User, user.id)

    assert user_db
    assert user_db.id == user.id
    assert user_db.username == custom_data["username"]
    assert user_db.email == custom_data["email"]
    assert user_db.level == custom_data["level"]
    assert user_db.height == custom_data["height"]
    assert user_db.is_active == custom_data["is_active"]
    assert user_db.birth_date == custom_data["birth_date"]


def test_user_sqlalchemy_factory_create_many(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
) -> None:
    count = 3

    users = user_sqlalchemy_factory.create_many(count)
    users_db = session.scalars(select(User)).all()

    assert len(users) == count
    assert len(users_db) == count
