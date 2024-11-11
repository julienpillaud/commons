from sqlalchemy import Select
from sqlalchemy.orm import noload

from app.application.schemas import PostCreate, PostUpdate
from app.domain.models import PostDomain, UserMinimalDomain
from app.infrastructure.exceptions import EntityNotFoundError
from app.infrastructure.models import Post, Tag, User
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class PostSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        Post,
        PostDomain,
        PostCreate,
        PostUpdate,
    ]
):
    model = Post
    schema = PostDomain

    def create(self, data: PostCreate, /) -> PostDomain:
        if not self.session.get(User, data.author_id):
            raise EntityNotFoundError("User", str(data.author_id))

        post = self.model(
            title=data.title,
            content=data.content,
            author_id=data.author_id,
            tags=[Tag(name=tag) for tag in data.tags],
        )

        self.session.add(post)
        self.session.commit()

        return self._to_domain(post)

    def _to_domain(self, model: Post, /, *, include_author: bool = True) -> PostDomain:
        return self.schema(
            id=model.id,
            title=model.title,
            content=model.content,
            author_id=model.author_id,
            author=UserMinimalDomain.model_validate(model.author)
            if include_author and model.author
            else None,
            tags=[tag.name for tag in model.tags],
        )

    def _apply_loading_options(
        self,
        stmt: Select[tuple[Post]],
        include_author: bool = True,
    ) -> Select[tuple[Post]]:
        if not include_author:
            stmt = stmt.options(noload(self.model.author))
        return stmt
