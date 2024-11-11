from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, StaticPool, create_engine
from sqlalchemy.orm import Session

from app.infrastructure.models import Base


@pytest.fixture
def engine() -> Engine:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    with Session(engine) as session:
        yield session
