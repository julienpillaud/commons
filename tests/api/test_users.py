import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.factories.user import UserSQLAlchemyFactory


def test_get_users(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    count = 3
    user_sqlalchemy_factory.create_many(count)

    response = client.get("/users/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == count
    assert data["limit"] == count
    assert len(data["items"]) == count


def test_get_users_with_pagination(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    total_users = 15
    page = 2
    limit = 5
    user_sqlalchemy_factory.create_many(total_users)

    response = client.get(f"/users/?page={page}&limit={limit}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == total_users
    assert data["limit"] == limit
    assert len(data["items"]) == limit


def test_get_user(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()

    response = client.get(f"/users/{created_user.id}")

    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["id"] == str(created_user.id)
    assert user["username"] == created_user.username
    assert user["email"] == created_user.email
    assert user["level"] == created_user.level
    assert user["height"] == created_user.height
    assert user["is_active"] == created_user.is_active
    assert user["birth_date"] == created_user.birth_date.isoformat()
    assert user["posts"] == []


def test_get_user_not_found(client: TestClient) -> None:
    user_id = uuid.uuid4()

    response = client.get(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_user(client: TestClient) -> None:
    user_data = {
        "username": "johndoe",
        "email": "john@example.com",
        "level": 1,
        "height": 180.0,
        "is_active": True,
        "birth_date": "1990-01-01",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    user = response.json()
    assert user["username"] == user_data["username"]
    assert user["email"] == user_data["email"]
    assert user["level"] == user_data["level"]
    assert user["height"] == user_data["height"]
    assert user["is_active"] == user_data["is_active"]
    assert user["birth_date"] == user_data["birth_date"]
    assert user["posts"] == []


def test_create_user_duplicate_email(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    existing_user = user_sqlalchemy_factory.create_one()
    user_data = {
        "username": "janedoe",
        "email": existing_user.email,
        "level": 1,
        "height": 170.0,
        "birth_date": "1990-01-01",
    }

    response = client.post("/users/", json=user_data)

    assert response.status_code == status.HTTP_409_CONFLICT


def test_update_user(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    update_data = {"height": created_user.height + 10}

    response = client.put(f"/users/{created_user.id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    user = response.json()
    assert user["id"] == str(created_user.id)
    assert user["height"] == update_data["height"]
    # Vérifie que les autres champs n'ont pas changé
    assert user["username"] == created_user.username
    assert user["email"] == created_user.email


def test_update_user_not_found(client: TestClient) -> None:
    user_id = uuid.uuid4()
    update_data = {"height": 190.0}

    response = client.put(f"/users/{user_id}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()

    response = client.delete(f"/users/{created_user.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_user_not_found(client: TestClient) -> None:
    user_id = uuid.uuid4()

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
