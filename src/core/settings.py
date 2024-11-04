from functools import cache
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Routine Generator API"
    version: str = "1.0.0"
    debug: bool = True
    openai_api_key: str


    model_config = SettingsConfigDict(env_file=".env")

@cache
def get_settings() -> Settings:
    return Settings()