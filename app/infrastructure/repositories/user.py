from app.application.schemas import UserCreate, UserUpdate
from app.domain.models import UserDomain
from app.infrastructure.models import User
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class UserSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        User,
        UserDomain,
        UserCreate,
        UserUpdate,
    ]
):
    model = User
    schema = UserDomain
