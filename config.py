from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field

PATH_DIR = Path(__file__).parent


class Settings(BaseSettings):
    DB_USER: str = Field(..., env='DB_USER')
    DB_PASS: str = Field(..., env='DB_PASS')
    DB_HOST: str = Field(..., env='DB_HOST')
    DB_PORT: str = Field(..., env='DB_PORT')
    DB_NAME: str = Field(..., env='DB_NAME')
    JWT_SECRET: str = Field(..., env='JWT_SECRET')
    JWT_ALGORITHM: str = Field(..., env='JWT_ALGORITHM')
    JWT_EXPIRE: int = Field(..., env='JWT_EXPIRE')

    class Config:
        env_file = f'{PATH_DIR}/.env'
        env_file_encoding = 'utf-8'

    def get_database_url(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    def get_test_db_url(self) -> str:
        return f'postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/test'


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
__all__ = ['settings']
