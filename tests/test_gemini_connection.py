import pytest
from app.core.config import settings
from app.services.factory import LLMFactory

def test_gemini_connection():
    """
    Testa apenas se a conexão com o Gemini é possível usando a credencial.
    Não valida cadeia completa de chat.
    """
    # Arrange
    llm = LLMFactory.create(provider="gemini")

    # Act
    response = llm.generate("Olá, isso é um teste de conexão. Responda apenas: OK.")

    # Assert
    assert "OK" in response.upper()

    print("\nFuncionou...")
