from pathlib import Path
from pydantic_settings import BaseSettings


class DbSettings(BaseSettings):
    DB_HOST:     str
    DB_PORT:     int
    DB_USER:     str
    DB_PASSWORD: str
    DB_NAME:     str

    @property
    def DB_URL_asyncpg(self):
        pass

    @property
    def DB_URL_psycopg(self):
        return f'postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    class Config:
        env_file = Path(__file__).resolve().parent.parent.parent / '.env'
        extra = "allow"

db_settings = DbSettings()
