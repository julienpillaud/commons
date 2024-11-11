import datetime
import uuid

import pytest
from sqlalchemy.orm import Session

from app.application.schemas import UserCreate, UserUpdate
from app.factories.user import UserSQLAlchemyFactory
from app.infrastructure.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
)
from app.infrastructure.models import User
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


def test_get_all(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    count = 3
    user_sqlalchemy_factory.create_many(count)

    results = user_repository.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_by_id(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()

    user = user_repository.get_by_id(created_user.id)

    assert user
    assert user.id == created_user.id
    assert user.username == created_user.username
    assert user.email == created_user.email
    assert user.level == created_user.level
    assert user.height == created_user.height
    assert user.is_active == created_user.is_active
    assert user.birth_date == created_user.birth_date
    assert user.posts == []


def test_get_by_id_not_found(user_repository: UserSQLAlchemyRepository) -> None:
    user_id = uuid.uuid4()

    with pytest.raises(EntityNotFoundError) as exc_info:
        user_repository.get_by_id(user_id)

    assert exc_info.value.args[0] == f"User {user_id} not found."


def test_create_user(
    session: Session,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    user_create = UserCreate(
        username="johndoe",
        email="john@example.com",
        level=1,
        height=180.0,
        is_active=True,
        birth_date=datetime.date(1990, 1, 1),
    )

    user = user_repository.create(user_create)
    user_db = session.get(User, user.id)

    assert user_db
    assert user_db.id == user.id
    assert user_db.username == user_create.username
    assert user_db.email == user_create.email
    assert user_db.level == user_create.level
    assert user_db.height == user_create.height
    assert user_db.is_active == user_create.is_active
    assert user_db.birth_date == user_create.birth_date
    assert user_db.posts == []


def test_create_user_already_exists(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    existing_user = user_sqlalchemy_factory.create_one()

    user_create = UserCreate(
        username="janedoe",
        email=existing_user.email,
        level=1,
        height=170.0,
        birth_date=datetime.date(1990, 1, 1),
    )

    with pytest.raises(EntityAlreadyExistsError) as exc_info:
        user_repository.create(user_create)

    assert exc_info.value.args[0] == "User already exists."


def test_update_user(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    new_height = created_user.height + 10
    user_update = UserUpdate(height=new_height)

    user = user_repository.update(created_user.id, user_update)
    user_db = session.get(User, user.id)

    assert user_db
    assert user_db.id == created_user.id
    assert user_db.username == created_user.username
    assert user_db.email == created_user.email
    assert user_db.level == created_user.level
    assert user_db.height == new_height
    assert user_db.is_active == created_user.is_active
    assert user_db.birth_date == created_user.birth_date
    assert user_db.posts == []


def test_update_user_not_found(user_repository: UserSQLAlchemyRepository) -> None:
    user_id = uuid.uuid4()
    user_update = UserUpdate(height=1.8)

    with pytest.raises(EntityNotFoundError) as exc_info:
        user_repository.update(user_id, user_update)

    assert exc_info.value.args[0] == f"User {user_id} not found."


def test_delete_user(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_repository: UserSQLAlchemyRepository,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()

    user_repository.delete(created_user.id)
    user_db = session.get(User, created_user.id)

    assert user_db is None


def test_delete_user_not_found(user_repository: UserSQLAlchemyRepository) -> None:
    user_id = uuid.uuid4()

    with pytest.raises(EntityNotFoundError) as exc_info:
        user_repository.delete(user_id)

    assert exc_info.value.args[0] == f"User {user_id} not found."
