from fastapi import APIRouter, HTTPException, status
from app.schemas.recordatorio import RecordatorioCreate, RecordatorioResponse, MessageResponse
from app.services.recordatorio_service import RecordatorioService
router = APIRouter(prefix="/api", tags=["recordatorios"])
service = RecordatorioService()
@router.get("/recordatorios", response_model=list[RecordatorioResponse])
def list_recordatorios():
    return service.list_recordatorios()
@router.get("/recordatorios/{recordatorio_id}", response_model=RecordatorioResponse)
def get_recordatorio(recordatorio_id: int):
    item = service.get_recordatorio(recordatorio_id)
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    return item
@router.get("/reservas/{reserva_id}/recordatorios", response_model=list[RecordatorioResponse])
def list_recordatorios_by_reserva(reserva_id: int):
    return service.list_by_reserva(reserva_id)
@router.post(
    "/recordatorios",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_recordatorio(data: RecordatorioCreate):
    service.create_recordatorio(data)
    return MessageResponse(mensaje="Recordatorio registrado correctamente")
@router.put("/recordatorios/{recordatorio_id}", response_model=MessageResponse)
def update_recordatorio(recordatorio_id: int, data: RecordatorioCreate):
    updated = service.update_recordatorio(recordatorio_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    return MessageResponse(mensaje="Recordatorio actualizado correctamente")
@router.delete("/recordatorios/{recordatorio_id}", response_model=MessageResponse)
def delete_recordatorio(recordatorio_id: int):
    deleted = service.delete_recordatorio(recordatorio_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    return MessageResponse(mensaje="Recordatorio eliminado correctamente")
@router.post(
    "/recordatorios/generar-para-reserva/{reserva_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def generar_recordatorios(reserva_id: int):
    result = service.generar_para_reserva(reserva_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada",
        )
    return MessageResponse(mensaje="Recordatorios generados correctamente para la reserva")