import boto3
import json
import os
from botocore.exceptions import ClientError

SECRET_NAME = "gemini_api_secret_name"

# A região onde o Secret está armazenado (deve ser a mesma do seu Fargate)
REGION_NAME = "us-east-2"

def get_gemini_api_key_from_secret():
    """
    Busca e extrai a chave da API Gemini do AWS Secrets Manager.
    """
    try:
        # 1. Cria a sessão do Boto3. O cliente do teste unitário simula esta chamada.
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=REGION_NAME
        )
        
        # 2. Obtém o valor do secret
        get_secret_value_response = client.get_secret_value(
            SecretId=SECRET_NAME
        )
        
    except ClientError as e:
        print(f"Erro ao acessar Secrets Manager: {e}")
        return None # Retorna None em caso de falha de conexão ou permissão

    # 3. Processamento do valor retornado
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        # Desserializa a string JSON para um dicionário Python
        secret_dict = json.loads(secret)
        
        # 4. Retorna o valor da chave específica
        if 'GEMINI_API_KEY' in secret_dict:
            return secret_dict['GEMINI_API_KEY']
        
    # Caso o formato esteja incorreto ou a chave não exista
    print("Erro: Chave 'GEMINI_API_KEY' não encontrada no Secret, ou Secret String não fornecida.")
    return None