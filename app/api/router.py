from fastapi import APIRouter

from app.api.routes.clientes import router as clientes_router 
from app.api.routes.paquetes import router as paquetes_router
from app.api.routes.paquetes_eventos import router as paquetes_eventos_router
from app.api.routes.detalle_reserva import router as detalle_reserva_router

api_router = APIRouter()
api_router.include_router(clientes_router)













# mi parte (patrick morales flores)

api_router.include_router(paquetes_router)
api_router.include_router(paquetes_eventos_router)
api_router.include_router(detalle_reserva_router)