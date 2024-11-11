import uuid

from fastapi import status
from fastapi.testclient import TestClient

from app.factories.post import PostSQLAlchemyFactory
from app.factories.user import UserSQLAlchemyFactory


def test_get_posts(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    client: TestClient,
) -> None:
    count = 3
    post_sqlalchemy_factory.create_many(count)

    response = client.get("/posts/")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == count
    assert data["limit"] == count
    assert len(data["items"]) == count


def test_get_posts_with_pagination(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    client: TestClient,
) -> None:
    total_posts = 15
    page = 2
    limit = 5
    post_sqlalchemy_factory.create_many(total_posts)

    response = client.get(f"/posts/?page={page}&limit={limit}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total"] == total_posts
    assert data["limit"] == limit
    assert len(data["items"]) == limit


def test_get_post(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    client: TestClient,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()

    response = client.get(f"/posts/{created_post.id}")

    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["id"] == str(created_post.id)
    assert post["title"] == created_post.title
    assert post["content"] == created_post.content
    assert post["author_id"] == str(created_post.author_id)
    assert set(post["tags"]) == set(created_post.tags)


def test_get_post_not_found(client: TestClient) -> None:
    post_id = uuid.uuid4()

    response = client.get(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_post(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    user = user_sqlalchemy_factory.create_one()
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content",
        "author_id": str(user.id),
        "tags": ["test", "python"],
    }

    response = client.post("/posts/", json=post_data)

    assert response.status_code == status.HTTP_201_CREATED
    post = response.json()
    assert post["title"] == post_data["title"]
    assert post["content"] == post_data["content"]
    assert post["author_id"] == post_data["author_id"]
    assert set(post["tags"]) == set(post_data["tags"])


def test_create_post_user_not_found(client: TestClient) -> None:
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content",
        "author_id": str(uuid.uuid4()),
        "tags": ["test", "python"],
    }

    response = client.post("/posts/", json=post_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_create_post_too_many_tags(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    client: TestClient,
) -> None:
    user = user_sqlalchemy_factory.create_one()
    post_data = {
        "title": "Test Post",
        "content": "This is a test post content",
        "author_id": str(user.id),
        "tags": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6"],
    }

    response = client.post("/posts/", json=post_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_update_post(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    client: TestClient,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()
    update_data = {"title": "Updated Post Title"}

    response = client.put(f"/posts/{created_post.id}", json=update_data)

    assert response.status_code == status.HTTP_200_OK
    post = response.json()
    assert post["id"] == str(created_post.id)
    assert post["title"] == update_data["title"]
    assert post["content"] == created_post.content
    assert post["author_id"] == str(created_post.author_id)
    assert set(post["tags"]) == set(created_post.tags)


def test_update_post_not_found(client: TestClient) -> None:
    post_id = uuid.uuid4()
    update_data = {"title": "Updated Post Title"}

    response = client.put(f"/posts/{post_id}", json=update_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_post(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    client: TestClient,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()

    response = client.delete(f"/posts/{created_post.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_post_not_found(client: TestClient) -> None:
    post_id = uuid.uuid4()

    response = client.delete(f"/posts/{post_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
