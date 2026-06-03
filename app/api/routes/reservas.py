from fastapi import APIRouter, HTTPException, status

from app.schemas.reserva import ReservaCreate, ReservaResponse, MessageResponse
from app.services.reserva_service import ReservaService


router = APIRouter(prefix="/api", tags=["reservas"])
service = ReservaService()


@router.get("/reservas", response_model=list[ReservaResponse])
def list_reservas():
    return service.list_reservas()


@router.get("/reservas/{reserva_id}", response_model=ReservaResponse)
def get_reserva(reserva_id: int):
    reserva = service.get_reserva(reserva_id)
    if reserva is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada",
        )
    return reserva


@router.get("/clientes/{cliente_id}/reservas", response_model=list[ReservaResponse])
def list_reservas_by_cliente(cliente_id: int):
    return service.list_by_cliente(cliente_id)


@router.post(
    "/reservas",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_reserva(data: ReservaCreate):
    service.create_reserva(data)
    return MessageResponse(mensaje="Reserva registrada correctamente")


@router.put("/reservas/{reserva_id}", response_model=MessageResponse)
def update_reserva(reserva_id: int, data: ReservaCreate):
    updated = service.update_reserva(reserva_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada",
        )
    return MessageResponse(mensaje="Reserva actualizada correctamente")


@router.delete("/reservas/{reserva_id}", response_model=MessageResponse)
def delete_reserva(reserva_id: int):
    deleted = service.delete_reserva(reserva_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada",
        )
    return MessageResponse(mensaje="Reserva eliminada correctamente")