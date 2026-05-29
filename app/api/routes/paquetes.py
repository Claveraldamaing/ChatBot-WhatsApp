from fastapi import APIRouter, HTTPException, status

from app.schemas.paquete import PaqueteCreate, PaqueteResponse, MessageResponse
from app.services.paquete_service import PaqueteService


router = APIRouter(prefix="/api", tags=["paquetes"])
service = PaqueteService()


@router.get("/paquetes", response_model=list[PaqueteResponse])
def list_paquetes():
    return service.list_paquetes()


@router.get("/paquetes/{paquete_id}", response_model=PaqueteResponse)
def get_paquete(paquete_id: int):
    paquete = service.get_paquete(paquete_id)
    if paquete is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado",
        )
    return paquete


@router.post(
    "/paquetes",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_paquete(paquete_data: PaqueteCreate):
    service.create_paquete(paquete_data)
    return MessageResponse(mensaje="Paquete registrado correctamente")


@router.put("/paquetes/{paquete_id}", response_model=MessageResponse)
def update_paquete(paquete_id: int, paquete_data: PaqueteCreate):
    updated = service.update_paquete(paquete_id, paquete_data)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado",
        )
    return MessageResponse(mensaje="Paquete actualizado correctamente")


@router.delete("/paquetes/{paquete_id}", response_model=MessageResponse)
def delete_paquete(paquete_id: int):
    deleted = service.delete_paquete(paquete_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paquete no encontrado",
        )
    return MessageResponse(mensaje="Paquete eliminado correctamente")