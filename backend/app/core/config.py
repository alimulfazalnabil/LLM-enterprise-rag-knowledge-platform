from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Enterprise RAG Knowledge Platform"
    app_env: str = "local"
    jwt_secret: str = "change-me-in-local-development"
    access_token_minutes: int = 30
    max_upload_size: int = 10 * 1024 * 1024
    dense_top_k: int = 20
    sparse_top_k: int = 20
    fusion_top_k: int = 20
    rerank_top_k: int = 8
    similarity_threshold: float = 0.05
    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


settings = Settings()
