import uuid
from typing import Any

from sqlalchemy.orm import Session

from app.domain.models import PostDomain, UserMinimalDomain
from app.factories.base import BaseDataFactory, BaseSQLAlchemyFactory, faker
from app.factories.user import UserDataFactory, UserSQLAlchemyFactory
from app.infrastructure.models import Post, Tag


class PostDataFactory(BaseDataFactory[PostDomain]):
    schema = PostDomain

    def __init__(self, user_data_factory: UserDataFactory) -> None:
        super().__init__()
        self.user_data_factory = user_data_factory

    def _fake_data(self, **kwargs: Any) -> dict[str, Any]:
        author = self.user_data_factory.create_one()
        minimal_author = UserMinimalDomain(
            id=author.id, username=author.username, email=author.email
        )
        nb_tags = faker.random_int(min=1, max=3)
        tags = [faker.unique.word() for _ in range(nb_tags)]
        return {
            "id": uuid.uuid4(),
            "title": faker.sentence(nb_words=6),
            "content": faker.paragraph(nb_sentences=10),
            "author_id": author.id,
            "author": minimal_author,
            "tags": tags,
        } | kwargs


class PostSQLAlchemyFactory(BaseSQLAlchemyFactory[PostDomain, Post]):
    schema = PostDomain
    model = Post
    # Override generic BaseDataFactory typing to access PostDataFactory attributes
    data_factory: PostDataFactory

    def __init__(
        self,
        session: Session,
        data_factory: PostDataFactory,
        user_sqlalchemy_factory: UserSQLAlchemyFactory,
    ) -> None:
        super().__init__(session=session, data_factory=data_factory)
        self.user_sqlalchemy_factory = user_sqlalchemy_factory

    def create_one(self, **kwargs: Any) -> PostDomain:
        post = self.data_factory.create_one(**kwargs)
        author_data = self.data_factory.user_data_factory.data[str(post.author_id)]
        self.user_sqlalchemy_factory.create_one(**author_data.model_dump())
        model = self._to_model(post)
        self.session.add(model)
        self.session.commit()
        return post

    def _to_model(self, entity: PostDomain) -> Post:
        return self.model(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            author_id=entity.author_id,
            tags=[Tag(name=tag) for tag in entity.tags],
        )
