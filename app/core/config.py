"""Este é o arquivo mais importante. Ele deve:

Parar de depender do .env na nuvem.

Ler as variáveis de configuração diretamente do os.environ (que o App Runner injeta).

Usar a função get_gemini_api_key_from_secret para preencher o campo GEMINI_API_KEY."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
from dotenv import load_dotenv
from app.core.aws_secrets import get_gemini_api_key_from_secret

# --- 1. Carregar Variáveis Locais para DEV ---
load_dotenv() 

class Settings(BaseSettings):
    APP_NAME: str = "Edu Assistente"

    # LÊ DIRETAMENTE DO os.environ (Injetado pelo App Runner)
    # Se o App Runner injetar ENV=production, ele sobrescreve o padrão.
    ENV: str = Field(os.environ.get("ENV", "local"), description="Ambiente da aplicação.") 

    # LÊ DIRETAMENTE DO os.environ
    LLM_PROVIDER: str = Field(
        os.environ.get("LLM_PROVIDER", "gemini"),
        description="Nome do provedor LLM a ser usado"
    )

    # LÊ DIRETAMENTE DO os.environ
    MODEL_NAME: str = Field(
        os.environ.get("MODEL_NAME", "models/gemini-1.5-flash-001"),
        description="Modelo padrão do provedor escolhido"
    )

    #Variável da API Key será resolvida pela lógica de nuvem/local
    GEMINI_API_KEY: str | None = None

    CORS_ORIGINS: List[str] = ["*"]


# --- 2. Lógica de Resolução da Chave ---

# Instância base (puxa tudo que é variável de ambiente)
settings = Settings()

# Se a chave foi fornecida localmente via .env, uss ela.
# Se não, tentamos puxar do Secrets Manager (só funciona na nuvem)
if settings.GEMINI_API_KEY is None:
    # 1. Tenta Secrets Manager (só funcionará no App Runner com a IAM Role)
    aws_key = get_gemini_api_key_from_secret()
    
    if aws_key:
        settings.GEMINI_API_KEY = aws_key
    
    # 2. Tenta a variável de ambiente do .env para desenvolvimento
    elif settings.ENV in ["local", "development"]:
        local_key = os.environ.get("GEMINI_API_KEY")
        if local_key:
             settings.GEMINI_API_KEY = local_key
        else:
             print("AVISO CRÍTICO: GEMINI_API_KEY não está no Secrets Manager nem no .env local!")


# Verifica se a chave foi resolvida antes de finalizar
if settings.GEMINI_API_KEY is None and settings.ENV not in ["local", "development"]:
     raise ValueError("Erro: GEMINI_API_KEY é obrigatória no ambiente de Produção.")