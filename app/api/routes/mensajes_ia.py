from fastapi import APIRouter, HTTPException, status
from app.schemas.mensaje_ia import MensajeIAResponse, MessageResponse
from app.services.mensajes_ia_service import MensajesIAService
router = APIRouter(prefix="/api", tags=["mensajes_ia"])
service = MensajesIAService()
@router.get("/clientes/{cliente_id}/mensajes", response_model=list[MensajeIAResponse])
def list_mensajes_by_cliente(cliente_id: int):
    return service.list_by_cliente(cliente_id)
@router.delete("/mensajes/{mensaje_id}", response_model=MessageResponse)
def delete_mensaje(mensaje_id: int):
    deleted = service.delete(mensaje_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensaje no encontrado",
        )
    return MessageResponse(mensaje="Mensaje eliminado correctamente") 