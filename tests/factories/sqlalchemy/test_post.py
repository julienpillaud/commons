from sqlalchemy import select
from sqlalchemy.orm import Session

from app.factories.post import PostSQLAlchemyFactory
from app.infrastructure.models import Post, User


def test_post_sqlalchemy_factory_create_one(
    session: Session,
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
) -> None:
    post = post_sqlalchemy_factory.create_one()
    post_db = session.get(Post, post.id)

    assert post_db
    assert post_db.id == post.id
    assert post_db.title == post.title
    assert post_db.content == post.content
    assert post_db.author_id == post.author_id
    assert {tag.name for tag in post_db.tags} == set(post.tags)

    user_db = session.get(User, post.author_id)
    assert user_db
    assert user_db.id == post.author_id


def test_post_sqlalchemy_factory_create_one_with_override(
    session: Session,
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
) -> None:
    custom_data = {
        "title": "Custom Title",
        "content": "Custom Content",
        "tags": ["tag1", "tag2"],
    }

    post = post_sqlalchemy_factory.create_one(**custom_data)
    post_db = session.get(Post, post.id)

    assert post_db
    assert post_db.id == post.id
    assert post_db.title == custom_data["title"]
    assert post_db.content == custom_data["content"]
    assert post_db.author_id == post.author_id
    assert {tag.name for tag in post_db.tags} == set(custom_data["tags"])

    user_db = session.get(User, post.author_id)
    assert user_db
    assert user_db.id == post.author_id


def test_post_sqlalchemy_factory_create_many(
    session: Session,
    post_sqlalchemy_factory: PostSQLAlchemyFactory,
) -> None:
    count = 3

    posts = post_sqlalchemy_factory.create_many(count)
    posts_db = session.scalars(select(Post)).all()
    users_db = session.scalars(select(User)).all()

    assert len(posts) == count
    assert len(posts_db) == count
    assert len(users_db) == count
