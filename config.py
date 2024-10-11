from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    ALLOWED_ORIGINS: list = ["http://localhost", "http://localhost:3000", "https://dogy-assistent.vercel.app/assistant"]
    openai_api_key: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()