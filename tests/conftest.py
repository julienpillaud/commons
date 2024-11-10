from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.factories.post import PostDataFactory, PostSQLAlchemyFactory
from app.factories.user import UserDataFactory, UserSQLAlchemyFactory
from app.infrastructure.models import Base
from app.infrastructure.repositories.post import PostSQLAlchemyRepository
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


@pytest.fixture
def engine() -> Engine:
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@pytest.fixture
def user_repository(session: Session) -> UserSQLAlchemyRepository:
    return UserSQLAlchemyRepository(session=session)


@pytest.fixture
def post_repository(session: Session) -> PostSQLAlchemyRepository:
    return PostSQLAlchemyRepository(session=session)


@pytest.fixture
def user_data_factory() -> UserDataFactory:
    return UserDataFactory()


@pytest.fixture
def post_data_factory(
    session: Session, user_data_factory: UserDataFactory
) -> PostDataFactory:
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
