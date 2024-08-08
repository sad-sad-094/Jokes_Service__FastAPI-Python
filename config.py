from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    jwt_secret: str = Field(alias="SECRET_KEY")
    jwt_algorithm: str = Field(alias="ALGORITHM")
    jwt_token_expo: int = Field(alias="ACCESS_TOKEN_EXPIRE_MINUTES")

    sql_url: str = Field(alias="SQLALCHEMY_DATABASE_URL")

    app_name: str = Field(alias="APP_NAME")

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
