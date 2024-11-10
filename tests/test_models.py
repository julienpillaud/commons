import datetime
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.models import Post, Tag, User


def test_user_creation(session: Session) -> None:
    user = User(
        username="johndoe",
        email="john@example.com",
        level=1,
        height=180.0,
        birth_date=datetime.date(1990, 1, 1),
    )
    session.add(user)
    session.commit()

    stmt = select(User).where(User.email == "john@example.com")
    result = session.execute(stmt).scalar_one()

    assert isinstance(result.id, uuid.UUID)
    assert result.username == user.username
    assert result.email == user.email
    assert result.level == user.level
    assert result.height == user.height
    assert result.is_active is True
    assert result.birth_date == user.birth_date
    assert result.posts == []


def test_post_creation(session: Session) -> None:
    user = User(
        username="johndoe",
        email="john@example.com",
        level=1,
        height=180.0,
        birth_date=datetime.date(1990, 1, 1),
    )
    session.add(user)
    session.commit()

    tag = Tag(name="python")
    post = Post(
        title="Test Post",
        content="Test Content",
        author_id=user.id,
        tags=[tag],
    )
    session.add(post)
    session.commit()

    stmt = select(Post).where(Post.title == "Test Post")
    result = session.execute(stmt).scalar_one()

    assert isinstance(result.id, uuid.UUID)
    assert result.title == post.title
    assert result.content == post.content
    assert result.author_id == user.id
    assert result.author == user
    result_tag = result.tags[0]
    assert isinstance(result_tag.id, uuid.UUID)
    assert result_tag.name == tag.name
