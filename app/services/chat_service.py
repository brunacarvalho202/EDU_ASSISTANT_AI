from app.services.llm_client import BaseLLMClient

class ChatService:
    """
    Camada de negócio do chat.
    Isola toda a lógica antes de chamar o LLM.
    """

    def __init__(self, llm_client: BaseLLMClient):
        self.llm = llm_client

    async def get_response(self, user_message: str) -> str:
        """
        Processa o prompt do usuário e delega ao LLM.
        """
        prompt = f"""
        Você é um assistente estudantil chamado EDU que vai atuar como um professor para qualquer pergunta no campo de ciência da computação.
        Usuário disse: "{user_message}"
        Responda de forma clara e direta.
        """

        return self.llm.generate(prompt)
