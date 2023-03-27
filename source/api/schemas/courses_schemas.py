from pydantic import Field

from .base_schemas import BaseModel


class CourseScheme(BaseModel):
    id: int
    name: str
    description: str


class CourseCreateScheme(BaseModel):
    name: str = Field(max_length=20)
    description: str = Field(default=None, max_length=250)


class CourseUpdateScheme(BaseModel):
    name: str = Field(default=None, max_length=20)
    description: str = Field(default=None, max_length=250)


