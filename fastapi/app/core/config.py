from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DEBUG: bool = False

    # Modern V2 configuration
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()