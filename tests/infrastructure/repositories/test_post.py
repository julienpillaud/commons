import uuid

import pytest
from sqlalchemy.orm import Session

from app.application.schemas import PaginationParams, PostCreate, PostUpdate
from app.factories.post import PostSQLAlchemyFactory
from app.factories.user import UserSQLAlchemyFactory
from app.infrastructure.exceptions import EntityNotFoundError
from app.infrastructure.models import Post
from app.infrastructure.repositories.post import PostSQLAlchemyRepository


def test_get_all(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    count = 3
    post_sqlalchemy_factory.create_many(count)

    results = post_repository.get_all()

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count


def test_get_all_with_pagination(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    count = 30
    page = 2
    limit = 10
    for i in range(count):
        post_sqlalchemy_factory.create_one(title=f"Post {i + 1}")

    results = post_repository.get_all(
        pagination=PaginationParams(page=page, limit=limit)
    )

    assert results.total == count
    assert results.limit == limit
    assert len(results.items) == limit

    expected_titles = [f"Post {i}" for i in range(11, 21)]
    actual_titles = [post.title for post in results.items]
    assert actual_titles == expected_titles


def test_get_all_without_author(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    count = 3
    post_sqlalchemy_factory.create_many(count)

    results = post_repository.get_all(include_author=False)

    assert results.total == count
    assert results.limit == count
    assert len(results.items) == count
    post = results.items[0]
    assert post.author is None


def test_get_all_with_pagination_without_author(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    count = 30
    limit = 10
    post_sqlalchemy_factory.create_many(count)

    results = post_repository.get_all(
        pagination=PaginationParams(limit=limit), include_author=False
    )

    assert results.total == count
    assert results.limit == limit
    assert len(results.items) == limit
    post = results.items[0]
    assert post.author is None


def test_get_by_id(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()

    post = post_repository.get_by_id(created_post.id)

    assert post
    assert post.id == created_post.id
    assert post.title == created_post.title
    assert post.content == created_post.content
    assert post.author_id == created_post.author_id

    assert post.author
    assert created_post.author
    assert post.author.id == created_post.author.id
    assert post.author.username == created_post.author.username
    assert post.author.email == created_post.author.email

    assert post.tags
    assert sorted(post.tags) == sorted(created_post.tags)


def test_get_by_id_without_author(
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()

    post = post_repository.get_by_id(created_post.id, include_author=False)

    assert post
    assert post.id == created_post.id
    assert post.title == created_post.title
    assert post.content == created_post.content
    assert post.author_id == created_post.author_id

    assert post.author is None


def test_get_by_id_not_found(post_repository: PostSQLAlchemyRepository) -> None:
    post_id = uuid.uuid4()

    with pytest.raises(EntityNotFoundError) as exc_info:
        post_repository.get_by_id(post_id)

    assert exc_info.value.args[0] == f"Post {post_id} not found."


def test_create_post(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    post_create = PostCreate(
        title="Test Post",
        content="Test Content",
        author_id=created_user.id,
        tags=["python"],
    )

    post = post_repository.create(post_create)
    post_db = session.get(Post, post.id)

    assert post_db
    assert post_db.id == post.id
    assert post_db.title == post_create.title
    assert post_db.content == post_create.content
    assert post_db.author_id == post_create.author_id

    assert post_db.author
    assert post_db.author.id == created_user.id
    assert post_db.author.username == created_user.username
    assert post_db.author.email == created_user.email

    assert post_db.tags
    assert sorted([tag.name for tag in post_db.tags]) == sorted(post_create.tags)


def test_post_create_duplicates_tags(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    post_create = PostCreate(
        title="Test Post",
        content="Test Content",
        author_id=created_user.id,
        tags=["python", "python", "fastapi"],
    )

    post = post_repository.create(post_create)
    post_db = session.get(Post, post.id)

    assert post_db
    assert sorted([tag.name for tag in post_db.tags]) == sorted(
        list(set(post_create.tags))
    )


def test_create_post_with_non_existent_user(
    post_repository: PostSQLAlchemyRepository,
) -> None:
    non_existent_user_id = uuid.uuid4()
    post_create = PostCreate(
        title="Test Post",
        content="Test Content",
        author_id=non_existent_user_id,
    )

    with pytest.raises(EntityNotFoundError) as exc_info:
        post_repository.create(post_create)

    assert exc_info.value.args[0] == f"User {non_existent_user_id} not found."


def test_update_post(
    session: Session,
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()
    post_update = PostUpdate(title="Updated Title")

    post = post_repository.update(created_post.id, post_update)
    post_db = session.get(Post, post.id)

    assert post_db
    assert post_db.id == created_post.id
    assert post_db.title == post_update.title
    assert post_db.content == created_post.content
    assert post_db.author_id == created_post.author_id

    assert post_db.author
    assert created_post.author
    assert post_db.author.id == created_post.author.id
    assert post_db.author.username == created_post.author.username
    assert post_db.author.email == created_post.author.email

    assert post_db.tags
    assert sorted([tag.name for tag in post_db.tags]) == sorted(created_post.tags)


def test_update_post_not_found(post_repository: PostSQLAlchemyRepository) -> None:
    post_id = uuid.uuid4()
    post_update = PostUpdate(title="Updated Title")

    with pytest.raises(EntityNotFoundError) as exc_info:
        post_repository.update(post_id, post_update)

    assert exc_info.value.args[0] == f"Post {post_id} not found."


def test_delete_post(
    session: Session,
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
    post_repository: PostSQLAlchemyRepository,
) -> None:
    created_post = post_sqlalchemy_factory.create_one()

    post_repository.delete(created_post.id)
    post_db = session.get(Post, created_post.id)

    assert post_db is None


def test_delete_post_not_found(post_repository: PostSQLAlchemyRepository) -> None:
    post_id = uuid.uuid4()

    with pytest.raises(EntityNotFoundError) as exc_info:
        post_repository.delete(post_id)

    assert exc_info.value.args[0] == f"Post {post_id} not found."
