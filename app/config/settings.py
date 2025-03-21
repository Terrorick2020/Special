from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    RESULTS_DIR: Path = Path("C:\\Users\\ta1\\Documents\\projects\\scaner\\app\\results")
    SUBDOMAINS_FILE: Path = Path("C:\\Users\\ta1\\Documents\\projects\\scaner\\app\\subdomains.txt")
    MAX_CONTENT_LINES: int = 500
    REQUEST_TIMEOUT: int = 15
    DEEPSEEK_API_KEY: str
    DEEPSEEK_MODEL: str = "google/gemma-3-12b-it:free"
    MAX_RETRIES: int = 3
    RETRY_DELAY: float = 1.0

    model_config = ConfigDict(
        env_file="app/.env",
        env_file_encoding="utf-8"
    )

    @field_validator("RESULTS_DIR", "SUBDOMAINS_FILE", mode="before")
    @classmethod
    def resolve_paths(cls, value: str | Path) -> Path:
        if isinstance(value, str):
            return Path(value).resolve()
        return value

settings = Settings()