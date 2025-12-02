import os
import json
import boto3
from dotenv import load_dotenv

# NENHUMA importação de app.core.aws_secrets deve estar aqui.

# O nome do Secret da AWS
AWS_SECRET_NAME = "chat-assistant-api-key" 

def get_gemini_api_key_from_secret() -> str | None:
    """
    Busca a GEMINI_API_KEY do AWS Secrets Manager, usando a IAM Role do App Runner.
    Aplica .strip() para limpar qualquer caractere invisível que a AWS possa injetar.
    """

    region_name = os.environ.get("AWS_REGION", "us-east-2") 
    
    # Se estiver em desenvolvimento local, evitamos falhar no Boto3
    if os.environ.get("ENV") in ["local", "development"]:
        return None 

    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    
    try:
        response = client.get_secret_value(SecretId=AWS_SECRET_NAME)
        
        # O valor é um JSON String, precisamos fazer o parse
        secret_json = json.loads(response['SecretString'])
        
        gemini_key = secret_json.get('GEMINI_API_KEY')
        
        if not gemini_key:
            print(f"ERRO: Chave 'GEMINI_API_KEY' não encontrada no JSON do Secret Manager.")
            return None
        
        # SEGURANÇA DUPLA: Limpamos a chave aqui também, removendo espaços e quebras de linha.
        return gemini_key.strip()

    except Exception as e:
        print(f"AVISO: Não foi possível obter Secret Manager. Presumindo ambiente LOCAL. Erro: {e}")
        return None