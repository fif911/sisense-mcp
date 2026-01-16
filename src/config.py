from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    sisense_base_url: str
    sisense_api_token: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
