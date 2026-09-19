import os
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Core Application Settings
    APP_ENV: str = "dev"
    DEBUG: bool = False

    # Postgres Credentials
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "postgres"
    POSTGRES_PORT: int = 5432

    # JWT Security Settings
    ALGORITHM: str = "HS256"  # or "RS256" for asymmetric
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 5

    # Dynamically build DATABASE_URL from individual variables
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    
    # Modern V2 configuration
    model_config = SettingsConfigDict(
        # 1. First check system environment variables
        # 2. If present (in Prod), load key/value pairs from the mounted secrets file
        env_file="/run/secrets/app.env" if os.path.exists("/run/secrets/app.env") else None,
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()