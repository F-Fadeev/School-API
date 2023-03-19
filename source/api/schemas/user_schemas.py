from pydantic import Field, EmailStr

from source.api.schemas.base_schemas import BaseModel


class UserSchema(BaseModel):
    name: str = Field(..., title='Имя пользователя')
    surname: str = Field(..., title='Фамилия пользователя')
    email: EmailStr = Field(..., title='Почта пользователя')
    is_active: bool = Field(True, title='Активность пользователя')
    password: str = Field(..., title='Пароль пользователя')

    class Config:
        schema_extra = {
            'example': {
                'name': 'Fedor',
                'surname': 'Ivanov',
                'email': 'fedor@google.com',
                'is_active': True,
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
