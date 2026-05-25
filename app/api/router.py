from fastapi import APIRouter

from app.api.routes.clientes import router as clientes_router


api_router = APIRouter()
api_router.include_router(clientes_router)
