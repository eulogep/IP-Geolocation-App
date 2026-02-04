from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    app_name: str = "EulogeServeur"
    circl_api_url: str = "https://ip.circl.lu"


@lru_cache
def get_settings() -> Settings:
    return Settings()
