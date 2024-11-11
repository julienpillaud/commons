import pytest
from sqlalchemy.orm import Session

from app.factories.post import PostDataFactory, PostSQLAlchemyFactory
from app.factories.user import UserDataFactory, UserSQLAlchemyFactory


@pytest.fixture
def user_data_factory() -> UserDataFactory:
    return UserDataFactory()


@pytest.fixture
def post_data_factory(user_data_factory: UserDataFactory) -> PostDataFactory:
    return PostDataFactory(user_data_factory=user_data_factory)


@pytest.fixture
def user_sqlalchemy_factory(
    session: Session, user_data_factory: UserDataFactory
) -> UserSQLAlchemyFactory:
    return UserSQLAlchemyFactory(session=session, data_factory=user_data_factory)


@pytest.fixture
def post_sqlalchemy_factory(
    session: Session,
    post_data_factory: PostDataFactory,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
) -> PostSQLAlchemyFactory:
    return PostSQLAlchemyFactory(
        session=session,
        data_factory=post_data_factory,
        user_sqlalchemy_factory=user_sqlalchemy_factory,
    )
