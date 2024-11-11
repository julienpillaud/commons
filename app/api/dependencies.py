from collections.abc import Iterator
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from app.application.services.post import PostService
from app.application.services.user import UserService
from app.core.config import Settings, get_settings
from app.infrastructure.repositories.post import PostSQLAlchemyRepository
from app.infrastructure.repositories.user import UserSQLAlchemyRepository


def get_database_uri(settings: Annotated[Settings, Depends(get_settings)]) -> str:
    return str(settings.SQLALCHEMY_DATABASE_URI)


@lru_cache
def get_engine(database_uri: Annotated[str, Depends(get_database_uri)]) -> Engine:
    return create_engine(database_uri)


def get_session(engine: Annotated[Engine, Depends(get_engine)]) -> Iterator[Session]:
    with Session(engine) as session:
        yield session


@lru_cache
def get_user_repository(
    session: Annotated[Session, Depends(get_session)],
) -> UserSQLAlchemyRepository:
    return UserSQLAlchemyRepository(session=session)


@lru_cache
def get_post_repository(
    session: Annotated[Session, Depends(get_session)],
) -> PostSQLAlchemyRepository:
    return PostSQLAlchemyRepository(session=session)


@lru_cache
def get_user_service(
    repository: Annotated[UserSQLAlchemyRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository=repository)


@lru_cache
def get_post_service(
    repository: Annotated[PostSQLAlchemyRepository, Depends(get_post_repository)],
) -> PostService:
    return PostService(repository=repository)
