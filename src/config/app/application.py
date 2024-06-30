from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_TITLE: str = "Meu Acervo Digital de Romances"
    PROJECT_VERSION: str = "0.0.1"
    DATABASE_URL: str = "sqlite:///database.db"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
