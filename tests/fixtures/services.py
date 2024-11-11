import pytest

from app.application.services.post import PostService
from app.application.services.user import UserService
from app.infrastructure.repositories.post import PostSQLAlchemyRepository
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


@pytest.fixture
def user_service(user_repository: UserSQLAlchemyRepository) -> UserService:
    return UserService(repository=user_repository)


@pytest.fixture
def post_service(post_repository: PostSQLAlchemyRepository) -> PostService:
    return PostService(repository=post_repository)
