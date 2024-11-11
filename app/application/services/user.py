from app.application.dtos import UserCreate, UserUpdate
from app.domain.models import UserDomain
from app.domain.service import AbstractService


class UserService(AbstractService[UserDomain, UserCreate, UserUpdate]):
    pass
