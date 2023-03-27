from pydantic import Field

from .base_schemas import BaseModel


class GroupScheme(BaseModel):
    id: int
    name: str


class GroupCreateScheme(BaseModel):
    name: str = Field(max_length=10)


class GroupUpdateScheme(BaseModel):
    name: str = Field(default=None, max_length=10)
