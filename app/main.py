from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.chat import router as chat_router

def create_app() -> FastAPI:
    """
    Cria a instância principal da aplicação FastAPI.
    Isolado em função para facilitar testes.
    """
    app = FastAPI(
        title="LLM Chat API",
        version="1.0.0",
        description="API modular para comunicação com modelos de linguagem.",
    )

    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rotas da aplicação
    app.include_router(chat_router)

    return app


app = create_app()

