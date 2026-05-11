# backend/app/core/config.py

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "fluxforge.db"


class Settings(BaseSettings):
    app_name: str = "FluxForge"

    debug: bool = True

    database_url: str = f"sqlite+aiosqlite:///{DB_PATH}"

    max_concurrent_downloads: int = 3
    max_concurrent_encodes: int = 2

    websocket_ping_interval: int = 20

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()