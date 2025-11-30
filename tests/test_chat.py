import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from services.llm_client import LLMClient


class FakeLLMClient(LLMClient):
    """
    Cliente fake para testes.
    Não chama nenhum LLM real.
    """

    async def generate(self, prompt: str) -> str:
        return f"RESPOSTA_FAKE: {prompt}"


@pytest.fixture
def test_app(monkeypatch):
    """
    Cria uma instância da aplicação substituindo o LLM real por um fake.
    Testes nunca devem chamar APIs externas.
    """

    def fake_container():
        class Container:
            llm_client = FakeLLMClient()
        return Container()

    # sobrescreve o container
    monkeypatch.setattr("core.container.get_container", fake_container)

    app = create_app()
    client = TestClient(app)
    return client


def test_chat_endpoint(test_app):
    """
    Testa o fluxo completo do endpoint /chat/respond
    usando cliente LLM fake.
    """

    payload = {"message": "Olá LLM!"}

    response = test_app.post("/chat/respond", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert "reply" in data
    assert data["reply"] == "RESPOSTA_FAKE: Olá LLM!"
