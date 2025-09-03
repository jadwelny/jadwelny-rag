from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_version: str
    OPENAI_API_KEY: str
    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int
    FILE_DEFAULT_CHUNK_SIZE: int
    MONGO_URL: str
    MONGO_DB_NAME: str
    class Config:
        env_file = ".env"

def get_settings():
    return Settings()
    