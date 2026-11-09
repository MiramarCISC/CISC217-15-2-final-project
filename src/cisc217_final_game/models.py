from __future__ import annotations
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class CharacterClass(Base):
    __tablename__="character_classes"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    characters: Mapped[list["Character"]]=relationship(back_populates="character_class")

class Character(Base):
    __tablename__="characters"
    id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]
    level: Mapped[int]=mapped_column(default=1)
    health: Mapped[int]=mapped_column(default=100)
    power: Mapped[int]=mapped_column(default=10)
    experience: Mapped[int]=mapped_column(default=0)
    class_id: Mapped[int]=mapped_column(ForeignKey("character_classes.id"))
    character_class: Mapped[CharacterClass]=relationship(back_populates="characters")
