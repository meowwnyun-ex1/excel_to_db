from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database Configuration
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "your_database"
    DB_USER: str = "your_user"
    DB_PASSWORD: str = "your_password"
    DB_TYPE: str = "postgresql"  # postgresql, mysql, sqlite

    # Processing Configuration
    BATCH_SIZE: int = 1000
    MAX_WORKERS: int = 4
    CHUNK_SIZE: int = 5000

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/excel_to_db.log"

    class Config:
        env_file = ".env"


settings = Settings()
