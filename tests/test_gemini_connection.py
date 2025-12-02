import pytest
import os
from app.core.config import settings
from app.services.factory import LLMFactory

# O teste só deve rodar em ambientes onde as credenciais AWS estão configuradas (Ex: local ou Fargate)
@pytest.mark.skipif(
    not os.environ.get("RUN_INTEGRATION_TESTS"),
    reason="Este teste requer que o ambiente de execução tenha permissões AWS para acessar Secrets Manager."
)
def test_gemini_connection():
    """
    Testa apenas se a conexão com o Gemini é possível usando a credencial
    resgatada.
    """
    # Arrange
    llm = LLMFactory.create(provider="gemini")

    # Act
    # Usamos uma consulta simples e barata
    response = llm.generate("Olá, isso é um teste de conexão. Responda apenas: OK.")

    # Assert
    assert "OK" in response.upper()
    print("\nTeste de conexão Gemini: Funcionou!")