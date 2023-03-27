from pydantic import Field, EmailStr

from source.api.schemas.base_schemas import BaseModel


class UserSchema(BaseModel):
    email: EmailStr = Field(..., title='Почта пользователя')
    password: str = Field(..., title='Пароль пользователя')

    class Config:
        schema_extra = {
            'example': {
                'email': 'fedor@google.com',
                'password': 'pAssw0rd',
            },
        }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            'example': {
                'email': 'fedor@google.com',
                'password': 'pAssw0rd',
            },
        }
