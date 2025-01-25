from src import Base, DateTimeWithTZ

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Text, Date, ForeignKey

from typing import Optional, List, TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from src.person import Person


class Film(Base):
    __tablename__ = "film_work"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    title: Mapped[str] = mapped_column(Text)
    description: Mapped[Optional[str]]
    creation_date: Mapped[Optional[Date]] = mapped_column(Date)
    file_path: Mapped[Optional[str]] = mapped_column(Text)
    rating: Mapped[float]
    type: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)
    updated_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)

    persons: Mapped[List["Person"]] = relationship(secondary="person_film_work", back_populates="films")
    genres: Mapped[List["Genre"]] = relationship(secondary="genre_film_work", back_populates="films")


class Genre(Base):
    __tablename__ = "genre"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    name: Mapped[str] = mapped_column(Text)
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)
    updated_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)

    films: Mapped[List[Film]] = relationship(secondary="genre_film_work", back_populates="genres")


class MovieGenreRelation(Base):
    __tablename__ = "genre_film_work"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    film_work_id: Mapped[str] = mapped_column(Text, ForeignKey("film_work.id"))
    genre_id: Mapped[str] = mapped_column(Text, ForeignKey("genre.id"))
    created_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)
