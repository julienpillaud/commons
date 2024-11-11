from app.application.dtos import PostCreate, PostUpdate
from app.domain.constants import PostConstants
from app.domain.exceptions import TooManyTagsError
from app.domain.models import PostDomain
from app.domain.service import AbstractService


class PostService(AbstractService[PostDomain, PostCreate, PostUpdate]):
    def create(self, data: PostCreate, /) -> PostDomain:
        cleaned_tags = self._clean_tags(data.tags)
        if len(cleaned_tags) > PostConstants.MAX_TAGS:
            raise TooManyTagsError(PostConstants.MAX_TAGS)

        cleaned_data = PostCreate(
            title=data.title.strip(),
            content=data.content,
            author_id=data.author_id,
            tags=cleaned_tags,
        )

        return super().create(cleaned_data)

    @staticmethod
    def _clean_tags(tags: list[str]) -> list[str]:
        cleaned = set()
        for tag in tags:
            if cleaned_tag := tag.lower().strip():
                cleaned.add(cleaned_tag)
        return sorted(cleaned)
