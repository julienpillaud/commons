class DomainError(Exception):
    pass


class PostError(DomainError):
    pass


class TooManyTagsError(PostError):
    def __init__(self, max_tags: int):
        self.max_tags = max_tags
        super().__init__(f"A post cannot have more than {max_tags} tags")
