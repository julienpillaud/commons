import pytest
from sqlalchemy.orm import Session

from app.infrastructure.repositories.post import PostSQLAlchemyRepository
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


@pytest.fixture
def user_repository(session: Session) -> UserSQLAlchemyRepository:
    return UserSQLAlchemyRepository(session=session)


@pytest.fixture
def post_repository(session: Session) -> PostSQLAlchemyRepository:
    return PostSQLAlchemyRepository(session=session)
