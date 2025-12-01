import unittest
import os
import json
from unittest.mock import patch, MagicMock

# Ajuste o caminho de importação conforme a estrutura do seu projeto
# O caminho correto deve ser: pasta_principal.pasta_app.pasta_core.nome_do_arquivo
from app.core.aws_secrets import get_gemini_api_key_from_secret

# --- Variáveis para Simulação (Mock) ---
# O valor que esperamos que a chave Gemini tenha
TEST_SECRET_VALUE = "MY_TEST_GEMINI_KEY_12345" 
# O JSON simulado que o Secrets Manager retornaria
TEST_SECRET_JSON = json.dumps({"GEMINI_API_KEY": TEST_SECRET_VALUE})


class SecretsManagerTest(unittest.TestCase):
    # --- Teste de Lógica: Verifica se o código extrai o valor corretamente ---
    def test_secret_value_extraction(self):
        """
        Testa se o código extrai corretamente a chave 'GEMINI_API_KEY'
        da string JSON retornada pelo Secrets Manager.
        """
        # 1. Simular o cliente do Secrets Manager
        mock_client = MagicMock()
        mock_client.get_secret_value.return_value = {
            'SecretString': TEST_SECRET_JSON
        }

        # 2. Substituir a chamada real do boto3 pela simulação (mock)
        with patch('boto3.session.Session.client', return_value=mock_client) as mock_boto_client:
            
            # 3. Chamar a função
            key = get_gemini_api_key_from_secret()

            # 4. Verificar o resultado esperado
            self.assertEqual(key, TEST_SECRET_VALUE)
            
            # 5. Verificação de chamada opcional: se o cliente foi chamado
            mock_boto_client.assert_called_once()


# --- Teste de Conexão REAL (Requer chaves AWS no terminal) ---
def run_real_connection_test():
    """
    Tenta uma conexão real com o AWS Secrets Manager para verificar a autenticação.
    """
    print("\n--- TESTE DE CONEXÃO REAL DA AWS ---")
    
    # ⚠️ Certifique-se de que o Secret 'chat-assistant-api-key' existe na região 'us-east-2'
    # e que suas credenciais estão definidas no terminal (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).
    
    try:
        real_key = get_gemini_api_key_from_secret()
        print(f"✅ SUCESSO! Chave Gemini REAL buscada. (Primeiros 5 caracteres: {real_key[:5]})")
        print("A autenticação do boto3 está funcionando corretamente no ambiente local.")
        return True
    except EnvironmentError as e:
        print(f"❌ ERRO CRÍTICO DE CONEXÃO: {e}")
        print("A autenticação do boto3 FALHOU. Verifique se:")
        print("1. O Secret 'chat-assistant-api-key' existe na região 'us-east-2'.")
        print("2. As variáveis AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY estão definidas no seu terminal.")
        return False


if __name__ == '__main__':
    # Primeiro, rodamos o teste de conexão real
    if run_real_connection_test():
        print("\n--- Testes Unitários de Lógica (Com Mocks) ---")
        # Se a conexão real funcionar, rodamos os testes de lógica
        unittest.main()
    else:
        # Se a conexão real falhar, podemos rodar os testes unitários de qualquer forma para validar a lógica
        # mas a aplicação falhará no Fargate por falta de acesso.
        print("\nO teste de conexão real FALHOU. Corrija as credenciais antes do push.")