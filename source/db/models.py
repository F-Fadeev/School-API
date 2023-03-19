
from sqlalchemy import (
    Column,
    ForeignKey,
    Table,
    String,
)
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)

from source.db.database import Base

association_table = Table(
    'association_table',
    Base.metadata,
    Column(
        'students_id',
        ForeignKey('students.id', ondelete='CASCADE'),
        primary_key=True,
    ),
    Column(
        'course_id',
        ForeignKey('courses.id', ondelete='CASCADE'),
        primary_key=True,
    ),
)


class Group(Base):
    __tablename__ = 'group'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)
    students: Mapped[list['Student']] = relationship()


class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey(
        'group.id',
        ondelete='SET NULL',
        onupdate='CASCADE'),
        nullable=True,
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(100), default='')
    courses: Mapped[list['Course']] = relationship(
        secondary=association_table,
        back_populates='students',
    )


class Course(Base):
    __tablename__ = 'courses'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(250), default='')
    students: Mapped[list[Student]] = relationship(
        secondary=association_table,
        back_populates='courses',
    )


class Users(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    surname: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

