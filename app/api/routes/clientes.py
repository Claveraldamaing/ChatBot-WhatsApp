from fastapi import APIRouter, HTTPException, status

from app.schemas.cliente import ClienteCreate, ClienteResponse, MessageResponse
from app.services.cliente_service import ClienteService


router = APIRouter(prefix="/api", tags=["clientes"])
service = ClienteService()


@router.get("/clientes", response_model=list[ClienteResponse])
def list_clientes():
    return service.list_clientes()


@router.get("/clientes/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int):
    cliente = service.get_cliente(cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return cliente


@router.post(
    "/clientes",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_cliente(cliente_data: ClienteCreate):
    service.create_cliente(cliente_data)
    return MessageResponse(mensaje="Cliente registrado correctamente")


@router.put("/clientes/{cliente_id}", response_model=MessageResponse)
def update_cliente(cliente_id: int, cliente_data: ClienteCreate):
    updated = service.update_cliente(cliente_id, cliente_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return MessageResponse(mensaje="Cliente actualizado correctamente")


@router.delete("/clientes/{cliente_id}", response_model=MessageResponse)
def delete_cliente(cliente_id: int):
    deleted = service.delete_cliente(cliente_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )
    return MessageResponse(mensaje="Cliente eliminado correctamente")
