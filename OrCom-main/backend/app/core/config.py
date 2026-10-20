
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
DEFAULT_DB_PATH: Path = BASE_DIR / "orcom.db"
DEFAULT_DB_URL: str = f"sqlite:///{DEFAULT_DB_PATH.as_posix()}"

# Vercel's deployed application directory is read-only.
# /tmp is writable, but its contents are temporary.
DEFAULT_STORAGE_DIR: Path = (
    Path("/tmp/orcom-storage")
    if os.getenv("VERCEL")
    else BASE_DIR / "storage"
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "OrCom Satellite Application Platform"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = DEFAULT_DB_URL

    # Active provider selection: 'mock' or 'dhruva'
    SATELLITE_PROVIDER: str = "mock"

    # Storage path for uploaded artifacts
    STORAGE_DIR: Path = DEFAULT_STORAGE_DIR

    # CORS configuration
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://127.0.0.1:3000"
    )
    CORS_ORIGIN_REGEX: str = r"^https:\/\/.*\.vercel\.app$"

    @property
    def cors_origins_list(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]


settings = Settings()

# Create the storage directory in a writable location.
settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
