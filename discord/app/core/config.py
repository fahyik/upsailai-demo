from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "FastAPI Server"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"


settings = Settings()
