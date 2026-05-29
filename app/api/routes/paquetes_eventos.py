from fastapi import APIRouter, HTTPException, status

from app.schemas.paquete_evento import PaqueteEventoCreate, PaqueteEventoResponse, MessageResponse
from app.services.paquete_evento_service import PaqueteEventoService


router = APIRouter(prefix="/api", tags=["paquetes_eventos"])
service = PaqueteEventoService()


@router.get("/paquetes-eventos", response_model=list[PaqueteEventoResponse])
def list_paquetes_eventos():
    return service.list_paquetes_eventos()


@router.get("/paquetes-eventos/{paquete_evento_id}", response_model=PaqueteEventoResponse)
def get_paquete_evento(paquete_evento_id: int):
    registro = service.get_paquete_evento(paquete_evento_id)
    if registro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacion paquete-evento no encontrada",
        )
    return registro


@router.get("/eventos/{evento_id}/paquetes", response_model=list[PaqueteEventoResponse])
def list_paquetes_by_evento(evento_id: int):
    return service.list_by_evento(evento_id)


@router.post(
    "/paquetes-eventos",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_paquete_evento(data: PaqueteEventoCreate):
    service.create_paquete_evento(data)
    return MessageResponse(mensaje="Relacion paquete-evento registrada correctamente")


@router.delete("/paquetes-eventos/{paquete_evento_id}", response_model=MessageResponse)
def delete_paquete_evento(paquete_evento_id: int):
    deleted = service.delete_paquete_evento(paquete_evento_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relacion paquete-evento no encontrada",
        )
    return MessageResponse(mensaje="Relacion paquete-evento eliminada correctamente")