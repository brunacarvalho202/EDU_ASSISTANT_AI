"""Este arquivo lida com a chave secreta da AWS (GEMINI_API_KEY) 
e as variáveis de configuração (lidas via os.environ.get() quando estiver no App Runner)."""

import os
import json
import boto3

# O nome do Secret que você criou na AWS
AWS_SECRET_NAME = "chat-assistant-api-key" 

def get_gemini_api_key_from_secret() -> str:
    """Busca a GEMINI_API_KEY do AWS Secrets Manager."""
    
    # Define a região (App Runner injeta isso, mas é bom ter um padrão)
    region_name = os.environ.get("AWS_REGION", "us_east-2") 
    
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=AWS_SECRET_NAME)
        # O valor do Secret vem como uma string JSON e contém a chave
        secret_json = json.loads(response['SecretString'])
        
        return secret_json.get('GEMINI_API_KEY')

    except Exception as e:
        # Se falhar no App Runner, é um erro crítico de permissão/acesso
        raise EnvironmentError(f"Falha ao carregar a chave Gemini do Secrets Manager: {e}")

def get_config_variables() -> dict:
    """Puxa as variáveis de configuração injetadas pelo App Runner."""
    
    return {
        "LLM_PROVIDER": os.environ.get("LLM_PROVIDER", "gemini"),
        "MODEL_NAME": os.environ.get("MODEL_NAME", "models/gemini-2.5-flash"),
        "ENV": os.environ.get("ENV", "production") 
    }