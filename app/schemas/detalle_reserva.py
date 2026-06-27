from pydantic import BaseModel
 
 
class DetalleReservaBase(BaseModel):
    idReservas: int
    idPaquetesEventos: int
    cantidad: int
    precio_unitario: float
    subtotal: float = 0
 
 
class DetalleReservaCreate(DetalleReservaBase):
    pass
 
 
class DetalleReservaResponse(DetalleReservaBase):
    id: int
    subtotal: float | None = None
 
    class Config:
        from_attributes = True
 
 
class MessageResponse(BaseModel):
    mensaje: str