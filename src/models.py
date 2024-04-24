from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


user_newsletter_table = sa.Table(
    "user_newsletter",
    Base.metadata,
    sa.Column("user_id", sa.ForeignKey("users.id"), primary_key=True),
    sa.Column("newsletter_id", sa.ForeignKey("newsletters.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    display_name: Mapped[str] = mapped_column(nullable=True)
    newsletters: Mapped[list[Newsletter]] = relationship(
        secondary=user_newsletter_table, back_populates="users"
    )


class Newsletter(Base):
    __tablename__ = "newsletters"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
    users: Mapped[list[User]] = relationship(
        secondary=user_newsletter_table, back_populates="newsletters"
    )
