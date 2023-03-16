
from pydantic import Field

from .base_schemas import BaseModel


class StudentScheme(BaseModel):
    id: int
    group_id: int = Field(default=None)
    first_name: str
    last_name: str
    middle_name: str = Field(default=None)


class StudentCreateScheme(BaseModel):
    group_id: int = Field(default=None)
    first_name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    middle_name: str = Field(max_length=100, default=None)


class StudentUpdateScheme(BaseModel):
    group_id: int = Field(default=None)
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    middle_name: str = Field(default=None)


class StudentsIdsScheme(BaseModel):
    student_ids: list[int]


class StudentFilters(BaseModel):
    first_name: str = Field(default=None)
    last_name: str = Field(default=None)
    middle_name: str = Field(default=None)
    group_id: int = Field(default=None)
    course_id: int = Field(default=None)
