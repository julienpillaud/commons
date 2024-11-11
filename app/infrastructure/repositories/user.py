from app.application.dtos import UserCreate, UserUpdate
from app.domain.models import PostDomain, UserDomain
from app.infrastructure.models import User
from app.infrastructure.repositories.base import SQLAlchemyRepositoryBase


class UserSQLAlchemyRepository(
    SQLAlchemyRepositoryBase[
        User,
        UserDomain,
        UserCreate,
        UserUpdate,
    ]
):
    model = User
    schema = UserDomain

    def _to_domain(self, model: User) -> UserDomain:
        return self.schema(
            id=model.id,
            username=model.username,
            email=model.email,
            level=model.level,
            height=model.height,
            is_active=model.is_active,
            birth_date=model.birth_date,
            posts=[
                PostDomain(
                    id=post.id,
                    title=post.title,
                    content=post.content,
                    author_id=post.author_id,
                    tags=[tag.name for tag in post.tags],
                )
                for post in model.posts
            ],
        )
