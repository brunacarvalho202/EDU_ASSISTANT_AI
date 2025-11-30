from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "Edu Assistente"

    ENV: str = Field("local", description="Ambiente da aplicação: local, dev, stg, prod")

    LLM_PROVIDER: str = Field(
        "gemini",
        description="Nome do provedor LLM a ser usado"
    )

    MODEL_NAME: str = Field(
        "gemini-1.5-flash-001",
        description="Modelo padrão do provedor escolhido"
    )

    GEMINI_API_KEY: str | None = None

    # 🔥 ADICIONE ISTO
    CORS_ORIGINS: List[str] = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
