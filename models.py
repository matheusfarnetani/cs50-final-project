from __future__ import annotations
from typing import List
from enum import Enum as Enumtype

from sqlalchemy import ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import Integer, String, Enum, Time, Date


class Base(DeclarativeBase):
    pass


# Create enum type to be used in 'cards' and 'users'
class Type(Enumtype):
    student = 'student'
    collaborator = 'collaborator'
    visitant = 'visitant'


# Instances's tables
class Arduinos(Base):
    __tablename__ = "arduinos"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    description: Mapped[str] = mapped_column(String(64))
    code_version: Mapped[str] = mapped_column(String(8), nullable=False)

    # Ont-to-one relation with 'equipments'
    # This table is the child
    equipment_id: Mapped[int] = mapped_column(Integer(), ForeignKey("equipments.id"), unique=True, index=True)
    equipment: Mapped["Equipments"] = relationship("Equipments", back_populates="arduino")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"arduino(id={self.id!r}, "
            f"description={self.description!r}, "
            f"code_version={self.code_version!r}, "
            f"equipment_id={self.equipment_id!r}, "
            f"equipment={self.equipment!r}"
        )


class Cards(Base):
    __tablename__ = "cards"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    uid: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    type: Mapped[Type] = mapped_column(Enum(Type), nullable=False, index=True)

    # One to one relation with table 'users'
    # This table is the parent
    user: Mapped["Users"] = relationship("Users", back_populates="card", uselist=False)

    # One-to-many relation with 'registers'
    register: Mapped[List["Registers"]] = relationship("Registers", back_populates="card")

    # One-to-one relation with table 'students'
    # This table is the parent
    student: Mapped["Students"] = relationship("Students", back_populates="card", uselist=False)

    # One-to-one relation with table 'collaborators'
    # This table is the parent
    collaborator: Mapped["Collaborators"] = relationship("Collaborators", back_populates="card", uselist=False)

    # One-to-many relation with table 'visitants'
    visitant: Mapped[List["Visitants"]] = relationship("Visitants", back_populates="card")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"card(id={self.id!r}, "
            f"uid={self.uid!r}, "
            f"type={self.type!r}, "
            f"user={self.user!r}, "
            f"register={self.register!r}, "
            f"student={self.student!r}, "
            f"collaborator={self.collaborator!r}, "
            f"visitant={self.visitant!r}, "
        )


class Collaborators(Base):
    __tablename__ = "collaborators"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    work_sector: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    work_shift_starts: Mapped[Time] = mapped_column(Time, nullable=False)
    work_shift_ends: Mapped[Time] = mapped_column(Time, nullable=False)

    # One-to-one relation with 'cards'
    # This table is the child
    card_id: Mapped[int] = mapped_column(Integer(), ForeignKey("cards.id"), unique=True, index=True)
    card: Mapped["Cards"] = relationship("Cards", back_populates="collaborator")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"student(id={self.id!r}, "
            f"name={self.name!r}, "
            f"birthday={self.birthday!r}, "
            f"work_sector={self.work_sector!r}, "
            f"work_shift_starts={self.work_shift_starts!r}), "
            f"work_shift_ends={self.work_shift_ends!r}), "
            f"card_id={self.card_id!r}), "
            f"card={self.card!r}"
        )


class Equipments(Base):
    __tablename__ = "equipments"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    description: Mapped[str] = mapped_column(String(64), nullable=False)
    eqp_type: Mapped[str] = mapped_column(String(32), nullable=False)
    date_last_inspection: Mapped[Date] = mapped_column(Date, nullable=False)
    date_next_inspection: Mapped[Date] = mapped_column(Date, nullable=False)

    # Many-to-one relation with 'places'
    place_id: Mapped[int] = mapped_column(Integer(), ForeignKey("places.id"), unique=True, index=True)
    place: Mapped["Places"] = relationship("Places", back_populates="equipment")

    # One-to-one relation with 'arduinos'
    # This table is the parent
    arduino: Mapped["Arduinos"] = relationship("Arduinos", back_populates="equipment", uselist=False)

    # One-to-many relation with 'registers'
    register: Mapped[List["Registers"]] = relationship("Registers", back_populates="equipment")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"equipment(id={self.id!r}, "
            f"description={self.description!r}, "
            f"eqp_type={self.eqp_type!r}, "
            f"date_last_inspection={self.date_last_inspection!r}, "
            f"date_next_inspection={self.date_next_inspection!r}), "
            f"place_id={self.place_id!r}), "
            f"place={self.place!r}), "
            f"arduino={self.arduino!r}), "
            f"register={self.register!r})"
        )


class Places(Base):
    __tablename__ = "places"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    description: Mapped[str] = mapped_column(String(32), nullable=False)

    # One-to-many relation with 'equipments'
    equipment: Mapped[List["Equipments"]] = relationship("Equipments", back_populates="place")
    
    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"place(id={self.id!r}), "
            f"description={self.description!r}, "
            f"equipment={self.equipment!r}"
        )


class Registers(Base):
    __tablename__ = "registers"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    date: Mapped[Date] = mapped_column(Date, nullable=False)
    hours: Mapped[int] = mapped_column(Integer(), nullable=False)
    minutes: Mapped[int] = mapped_column(Integer(), nullable=False)
    seconds: Mapped[int] = mapped_column(Integer(), nullable=False)

    # Many-to-one relation with 'cards'
    card_id: Mapped[int] = mapped_column(Integer(), ForeignKey("cards.id"), index=True)
    card: Mapped["Cards"] = relationship("Cards", back_populates="register")

    # Many-to-one relation with 'equipments'
    equipment_id: Mapped[int] = mapped_column(Integer(), ForeignKey("equipments.id"), index=True)
    equipment: Mapped["Equipments"] = relationship("Equipments", back_populates="register")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"register(id={self.id!r}, "
            f"date={self.date!r}, "
            f"hours={self.hours!r}, "
            f"minutes={self.minutes!r}, "
            f"seconds={self.seconds!r}), "
            f"card_id={self.card_id!r}), "
            f"card={self.card!r}), "
            f"equipment_id={self.equipment_id!r}), "
            f"equipment={self.equipment!r}), "
        )


class Students(Base):
    __tablename__ = "students"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    course: Mapped[str] = mapped_column(String(128), nullable=False)
    course_start: Mapped[Date] = mapped_column(Date, nullable=False)

    # One-to-one relation with 'cards'
    # This table is the child
    card_id: Mapped[int] = mapped_column(Integer(), ForeignKey("cards.id"), unique=True, index=True)
    card: Mapped["Cards"] = relationship("Cards", back_populates="student")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"student(id={self.id!r}, "
            f"name={self.name!r}, "
            f"birthday={self.birthday!r}, "
            f"course={self.course!r}, "
            f"course_start={self.course_start!r}), "
            f"card_id={self.card_id!r}), "
            f"card={self.card!r})"
        )


class Users(Base):
    __tablename__ = "users"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    type: Mapped[Type] = mapped_column(Enum(Type), nullable=False, index=True)
    hash: Mapped[str] = mapped_column(String(64), nullable=False)

    # One to one relation with table 'cards'
    # This table is the child
    card_id: Mapped[int] = mapped_column(Integer(), ForeignKey("cards.id"), unique=True, index=True)
    card: Mapped["Cards"] = relationship("Cards", back_populates="user")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"user(id={self.id!r}, "
            f"username={self.username!r}, "
            f"email={self.email!r}, "
            f"user_type={self.user_type!r}, "
            f"card_id={self.card_id!r}, "
            f"card={self.card!r}"
        )


class Visitants(Base):
    __tablename__ = "visitants"

    # Attributes
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    birthday: Mapped[Date] = mapped_column(Date, nullable=False)
    document: Mapped[str] = mapped_column(String(64), nullable=False)

    # Many-to-one relation with table 'cards'
    card_id: Mapped[int] = mapped_column(Integer(), ForeignKey("cards.id"), index=True)
    card: Mapped["Cards"] = relationship("Cards", back_populates="visitant")

    # Allow readable string output
    def __repr__(self) -> str:
        return (
            f"visitant(id={self.id!r}, "
            f"name={self.name!r}, "
            f"birthday={self.birthday!r}, "
            f"document={self.document!r}, "
            f"card_id={self.card_id!r}, "
            f"card={self.card!r}"
        )
