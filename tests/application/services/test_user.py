import datetime

from app.application.schemas import UserCreate, UserUpdate
from app.application.services.user import UserService
from app.factories.user import UserSQLAlchemyFactory


def test_get_all(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_service: UserService,
) -> None:
    count = 3
    user_sqlalchemy_factory.create_many(count)

    results = user_service.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_by_id(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_service: UserService,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()

    user = user_service.get_by_id(created_user.id)

    assert user.id == created_user.id
    assert user.username == created_user.username
    assert user.email == created_user.email
    assert user.level == created_user.level
    assert user.height == created_user.height
    assert user.is_active == created_user.is_active
    assert user.birth_date == created_user.birth_date
    assert user.posts == []


def test_create_user(user_service: UserService) -> None:
    user_create = UserCreate(
        username="johndoe",
        email="john@example.com",
        level=1,
        height=180.0,
        is_active=True,
        birth_date=datetime.date(1990, 1, 1),
    )

    user = user_service.create(user_create)

    assert hasattr(user, "id")
    assert user.username == user_create.username
    assert user.email == user_create.email
    assert user.level == user_create.level
    assert user.height == user_create.height
    assert user.is_active == user_create.is_active
    assert user.birth_date == user_create.birth_date
    assert user.posts == []


def test_update_user(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    user_service: UserService,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    new_height = created_user.height + 10
    user_update = UserUpdate(height=new_height)

    user = user_service.update(created_user.id, user_update)

    assert user.id == created_user.id
    assert user.username == created_user.username
    assert user.email == created_user.email
    assert user.level == created_user.level
    assert user.height == new_height
    assert user.is_active == created_user.is_active
    assert user.birth_date == created_user.birth_date
    assert user.posts == []
