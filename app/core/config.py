from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DEBUG: bool = False
    SECRET_KEY: str = "change-this-to-a-very-long-random-string"  # openssl rand -hex 32
    ALGORITHM: str = "HS256"  # or "RS256" for asymmetric
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 5


    # Modern V2 configuration
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()