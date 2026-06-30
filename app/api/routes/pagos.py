
from fastapi import APIRouter, HTTPException, status
 
from app.schemas.pago import PagoCreate, PagoResponse, MessageResponse,PagoUpdateEstado
from app.services.pago_service import PagoService
 
 
router = APIRouter(prefix="/api", tags=["pagos"])
service = PagoService()
 
 
@router.get("/pagos", response_model=list[PagoResponse])
def list_pagos():
    return service.list_pagos()
 
 
@router.get("/pagos/{pago_id}", response_model=PagoResponse)
def get_pago(pago_id: int):
    pago = service.get_pago(pago_id)
    if pago is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )
    return pago
 
 
@router.get("/reservas/{reserva_id}/pagos", response_model=list[PagoResponse])
def list_pagos_by_reserva(reserva_id: int):
    return service.list_by_reserva(reserva_id)
 
 
@router.post(
    "/pagos",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_pago(data: PagoCreate):
    service.create_pago(data)
    return MessageResponse(mensaje="Pago registrado correctamente")
 
 
@router.put("/pagos/{pago_id}", response_model=MessageResponse)
def update_pago(pago_id: int, data: PagoCreate):
    updated = service.update_pago(pago_id, data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )
    return MessageResponse(mensaje="Pago actualizado correctamente")
 
 
@router.delete("/pagos/{pago_id}", response_model=MessageResponse)
def delete_pago(pago_id: int):
    deleted = service.delete_pago(pago_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )
    return MessageResponse(mensaje="Pago eliminado correctamente")
 
@router.put("/pagos/{pago_id}/confirmar", response_model=MessageResponse)
def confirmar_pago(pago_id: int):
    result = service.confirmar_pago(pago_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pago no encontrado",
        )
    return MessageResponse(mensaje="Pago confirmado y reserva actualizada a confirmada")