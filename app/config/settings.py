from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: str = "5432"
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    RESULTS_DIR: Path = Path("results")
    SUBDOMAINS_FILE: Path = Path("subdomains.txt")
    MAX_CONTENT_LINES: int = 500
    REQUEST_TIMEOUT: int = 15
    DEEPSEEK_API_KEY: str
    DEEPSEEK_MODEL: str = "google/gemma-3-12b-it:free"
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0
    REDIS_URL: str = "redis://redis:6379/0"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    @field_validator("RESULTS_DIR", "SUBDOMAINS_FILE", mode="before")
    @classmethod
    def resolve_paths(cls, value: str | Path) -> Path:
        if isinstance(value, str):
            return Path(value).resolve()
        return value

settings = Settings()