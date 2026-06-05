from fastapi import APIRouter, HTTPException, status
 
from app.schemas.evento import EventoCreate, EventoResponse, MessageResponse
from app.services.evento_service import EventoService
 
 
router = APIRouter(prefix="/api", tags=["eventos"])
service = EventoService()
 
 
@router.get("/eventos", response_model=list[EventoResponse])
def list_eventos():
    return service.list_eventos()
 
 
@router.get("/eventos/{evento_id}", response_model=EventoResponse)
def get_evento(evento_id: int):
    evento = service.get_evento(evento_id)
    if evento is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    return evento
 
 
@router.post(
    "/eventos",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_evento(data: EventoCreate):
    service.create_evento(data)
    return MessageResponse(mensaje="Evento registrado correctamente")
 
 
@router.put("/eventos/{evento_id}", response_model=MessageResponse)
def update_evento(evento_id: int, data: EventoCreate):
    updated = service.update_evento(evento_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    return MessageResponse(mensaje="Evento actualizado correctamente")
 
 
@router.delete("/eventos/{evento_id}", response_model=MessageResponse)
def delete_evento(evento_id: int):
    deleted = service.delete_evento(evento_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento no encontrado",
        )
    return MessageResponse(mensaje="Evento eliminado correctamente")
 