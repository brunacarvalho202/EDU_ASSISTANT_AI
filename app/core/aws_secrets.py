from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os
from dotenv import load_dotenv
from app.core.aws_secrets import get_gemini_api_key_from_secret

# --- 1. Carregar Variáveis Locais para DEV ---
# Isso só terá efeito no ambiente 'local' onde o arquivo .env existe.
# Não afeta o ambiente de nuvem (App Runner/ECS).
load_dotenv() 

class Settings(BaseSettings):
    APP_NAME: str = "Edu Assistente"

    # LÊ DIRETAMENTE DO os.environ (Injetado pela nuvem)
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

    # Variável da API Key: Não inicializada pela classe, será resolvida na lógica abaixo.
    GEMINI_API_KEY: str | None = None

    CORS_ORIGINS: List[str] = ["*"]


# --- 2. Lógica de Resolução da Chave ---

# Instância base (puxa tudo que é variável de ambiente)
settings = Settings()

# Se a chave não foi resolvida (o que é esperado)
if settings.GEMINI_API_KEY is None:
    
    # 1. Tenta Secrets Manager (Prioridade na nuvem)
    aws_key = get_gemini_api_key_from_secret()
    
    if aws_key:
        # CORREÇÃO CRÍTICA: Aplica o .strip() para limpar espaços/quebras de linha do AWS Secret
        settings.GEMINI_API_KEY = aws_key.strip() 
    
    # 2. Tenta a variável de ambiente local (apenas para desenvolvimento)
    elif settings.ENV in ["local", "development"]:
        # Lê a chave do ambiente local (do .env) e a limpa imediatamente.
        local_key = os.environ.get("GEMINI_API_KEY")
        
        if local_key:
            # CORREÇÃO CRÍTICA: Aplica o .strip() para limpar espaços/quebras de linha do .env
            settings.GEMINI_API_KEY = local_key.strip()
        else:
            print("AVISO CRÍTICO: GEMINI_API_KEY não está no Secrets Manager nem no .env local!")


# Verifica se a chave foi resolvida antes de finalizar
if not settings.GEMINI_API_KEY:
    # Levanta erro se a chave não foi resolvida em NENHUM ambiente
    if settings.ENV in ["local", "development"]:
        raise ValueError("Erro: GEMINI_API_KEY é obrigatória no ambiente de Desenvolvimento (via .env).")
    else:
        # Melhorando a mensagem de erro para o App Runner/ECS
        raise ValueError(
            "Erro: GEMINI_API_KEY é obrigatória no ambiente de Produção. "
            "Verifique se o Secret Manager está configurado corretamente e se a IAM Role possui permissão de leitura."
        )