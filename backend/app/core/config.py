from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = 'development'
    database_url: str = '******localhost:5432/rag'
    redis_url: str = 'redis://localhost:6379/0'
    jwt_secret: str = 'change-me'

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()
