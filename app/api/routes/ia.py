from fastapi import APIRouter

from app.schemas.ia import MensajeIA, RespuestaIA
from app.services.ia_service import IAService


router = APIRouter(prefix="/api", tags=["ia"])
service = IAService()


@router.post("/ia", response_model=RespuestaIA)
def consultar_ia(data: MensajeIA):
    respuesta = service.responder(data.texto, data.session_id)

    return RespuestaIA(
        session_id=data.session_id,
        mensaje_recibido=data.texto,
        respuesta_ia=respuesta
    )