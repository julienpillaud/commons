import datetime
import uuid

from sqlalchemy import Column, ForeignKey, Table, Uuid
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4
    )


post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id"), primary_key=True),
)


class User(Base):
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    level: Mapped[int]
    height: Mapped[float]
    is_active: Mapped[bool] = mapped_column(default=True)
    birth_date: Mapped[datetime.date]

    posts: Mapped[list["Post"]] = relationship(back_populates="author")


class Post(Base):
    title: Mapped[str]
    content: Mapped[str]
    author_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("user.id"))

    author: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship(secondary=post_tags)


class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True)
