from fastapi import APIRouter, HTTPException, status
from app.schemas.recordatorio import RecordatorioCreate, RecordatorioResponse, MessageResponse
from app.services.recordatorio_service import RecordatorioService
router = APIRouter(prefix="/api", tags=["recordatorios"])
service = RecordatorioService()
@router.get("/recordatorios", response_model=list[RecordatorioResponse])
def list_recordatorios():
    return service.list_recordatorios()
@router.get("/recordatorios/pendientes-para-enviar")
def pendientes_para_enviar():
    pendientes = service.repository.get_pendientes()
    resultado = []
    for r in pendientes:
        from app.repositories.reserva_repository import ReservaRepository
        from app.repositories.cliente_repository import ClienteRepository
        reserva_repo = ReservaRepository()
        cliente_repo = ClienteRepository()
        reserva = reserva_repo.get_by_id(r[1])
        if not reserva:
            continue
        cliente = cliente_repo.get_by_id(reserva[1])
        if not cliente:
            continue
        resultado.append({
            "id": r[0],
            "idReserva": r[1],
            "tipo": r[2],
            "mensaje": r[3],
            "telefono": cliente[2],
            "fecha_programada": str(r[4]),
        })
    return resultado
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
@router.patch("/recordatorios/{recordatorio_id}/enviar", response_model=MessageResponse)
def marcar_enviado(recordatorio_id: int):
    updated = service.marcar_enviado(recordatorio_id)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recordatorio no encontrado",
        )
    return MessageResponse(mensaje="Recordatorio marcado como enviado")
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

