from fastapi import APIRouter
from app.api.routes.ia import router as ia_router

from app.api.routes.clientes import router as clientes_router 
from app.api.routes.paquetes import router as paquetes_router
from app.api.routes.paquetes_eventos import router as paquetes_eventos_router
from app.api.routes.detalle_reserva import router as detalle_reserva_router
from app.api.routes.eventos import router as eventos_router
from app.api.routes.reservas import router as reservas_router
from app.api.routes.pagos import router as pagos_router

api_router = APIRouter()
api_router.include_router(clientes_router)

#erick
api_router.include_router(ia_router)












# mi parte (patrick morales flores)

api_router.include_router(paquetes_router)
api_router.include_router(paquetes_eventos_router)
api_router.include_router(detalle_reserva_router)
api_router.include_router(eventos_router)
api_router.include_router(reservas_router)
api_router.include_router(pagos_router)
