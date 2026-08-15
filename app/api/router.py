from fastapi import APIRouter
from app.api.v1.users import router as user_router
from app.api.v1.auth import router as auth_router
from app.api.v1.modules import router as module_router
from app.api.v1.upload import router as upload_router
from app.api.v1.files import router as file_router
from app.api.v1.conversations import router as conversation_router  


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(module_router)
api_router.include_router(upload_router)
api_router.include_router(file_router)
api_router.include_router(conversation_router) 