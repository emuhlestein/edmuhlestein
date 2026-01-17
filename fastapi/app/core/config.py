from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"

    # Modern V2 configuration
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()