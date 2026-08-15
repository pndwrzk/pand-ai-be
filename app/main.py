from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import settings
from app.db.qdrant import Qdrant
from app.exceptions.handlers import register_exception_handlers
from app.messaging.rabbitmq import RabbitMQ
from app.rag.embedding import Embedding


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rabbitmq = RabbitMQ()
    app.state.qdrant = Qdrant()
    Embedding()

    yield

    app.state.rabbitmq.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
   allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)

app.include_router(api_router)


@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "FastAPI Starter Running"
    }