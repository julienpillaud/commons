from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.api.dependencies import get_session
from app.main import app


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()
