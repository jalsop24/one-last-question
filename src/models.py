from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str]
    display_name: Mapped[str] = mapped_column(nullable=True)


class Newsletter(Base):
    __tablename__ = "newsletters"
    id: Mapped[int] = mapped_column(primary_key=True)
    content: Mapped[str]
