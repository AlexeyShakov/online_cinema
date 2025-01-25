from typing import List, TYPE_CHECKING

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Text, ForeignKey

from src import Base, DateTimeWithTZ
from datetime import datetime


if TYPE_CHECKING:
    from src.films.models import Film


class Person(Base):
    __tablename__ = "person"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    full_name: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)
    updated_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)

    films: Mapped[List["Film"]] = relationship(secondary="person_film_work", back_populates="persons")


class PersonFilmRelation(Base):
    __tablename__ = "person_film_work"

    id: Mapped[str] = mapped_column(Text, primary_key=True)
    film_work_id: Mapped[str] = mapped_column(Text, ForeignKey("film_work.id"))
    person_id: Mapped[str] = mapped_column(Text, ForeignKey("person.id"))
    role: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTimeWithTZ)
