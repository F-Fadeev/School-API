
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field


class BaseModel(PydanticBaseModel):
    class Config:
        orm_mode = True


class ErrorResponseScheme(BaseModel):
    detail: str = Field(
        ...,
        title='Подробнее об ошибке',
    )

    class Config:
        schema_extra = {
            'example': {'detail': 'HTTPException raised.'},
        }


class DefaultResponseScheme(BaseModel):
    detail: str



