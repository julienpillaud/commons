import pytest

from app.application.schemas import PostCreate
from app.application.services.post import PostService
from app.domain.constants import PostConstants
from app.domain.exceptions import TooManyTagsError
from app.factories.user import UserSQLAlchemyFactory


def test_create_post(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    post_service: PostService,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    post_create = PostCreate(
        title="Test Post",
        content="Test Content",
        author_id=created_user.id,
        tags=["python", "fastapi"],
    )

    post = post_service.create(post_create)

    assert hasattr(post, "id")
    assert post.title == post_create.title
    assert post.content == post_create.content
    assert post.author_id == post_create.author_id

    assert post.author
    assert post.author.id == created_user.id
    assert post.author.username == created_user.username
    assert post.author.email == created_user.email

    assert set(post.tags) == set(post_create.tags)


def test_create_post_messy_tags(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    post_service: PostService,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    post_create = PostCreate(
        title="Test Post",
        content="Test Content",
        author_id=created_user.id,
        tags=[
            "Python  ",
            "python",
            "  FastAPI",
            "API",
            "",
            "  ",
        ],
    )

    post = post_service.create(post_create)

    assert set(post.tags) == {"python", "fastapi", "api"}


def test_create_post_too_many_tags(
    user_sqlalchemy_factory: UserSQLAlchemyFactory,
    post_service: PostService,
) -> None:
    created_user = user_sqlalchemy_factory.create_one()
    post_create = PostCreate(
        title="Test Post",
        content="Test Content",
        author_id=created_user.id,
        tags=[f"tag{i}" for i in range(PostConstants.MAX_TAGS + 1)],
    )

    with pytest.raises(TooManyTagsError) as exc_info:
        post_service.create(post_create)

    assert exc_info.value.max_tags == PostConstants.MAX_TAGS
