from fastapi import APIRouter, HTTPException, status

from app.schemas.detalle_reserva import DetalleReservaCreate, DetalleReservaResponse, MessageResponse
from app.services.detalle_reserva_service import DetalleReservaService


router = APIRouter(prefix="/api", tags=["detalle_reserva"])
service = DetalleReservaService()


@router.get("/detalle-reserva", response_model=list[DetalleReservaResponse])
def list_detalles():
    return service.list_detalles()


@router.get("/detalle-reserva/{detalle_id}", response_model=DetalleReservaResponse)
def get_detalle(detalle_id: int):
    detalle = service.get_detalle(detalle_id)
    if detalle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detalle de reserva no encontrado",
        )
    return detalle


@router.get("/reservas/{reserva_id}/detalle", response_model=list[DetalleReservaResponse])
def list_detalle_by_reserva(reserva_id: int):
    return service.list_by_reserva(reserva_id)


@router.post(
    "/detalle-reserva",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_detalle(data: DetalleReservaCreate):
    service.create_detalle(data)
    return MessageResponse(mensaje="Detalle de reserva registrado correctamente")


@router.put("/detalle-reserva/{detalle_id}", response_model=MessageResponse)
def update_detalle(detalle_id: int, data: DetalleReservaCreate):
    updated = service.update_detalle(detalle_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detalle de reserva no encontrado",
        )
    return MessageResponse(mensaje="Detalle de reserva actualizado correctamente")


@router.delete("/detalle-reserva/{detalle_id}", response_model=MessageResponse)
def delete_detalle(detalle_id: int):
    deleted = service.delete_detalle(detalle_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detalle de reserva no encontrado",
        )
    return MessageResponse(mensaje="Detalle de reserva eliminado correctamente")