from datetime import datetime
from pydantic import BaseModel
class MensajeIABase(BaseModel):
    idClientes: int
    rol: str
    contenido: str
    tipo: str | None = None
    estado: str = "activo"
    tiene_reserva: bool = False
class MensajeIACreate(MensajeIABase):
    pass
class MensajeIAResponse(MensajeIABase):
    id: int
    fecha_hora_mensaje: datetime | None = None
    class Config:
        from_attributes = True
class MensajeIAClienteFilter(BaseModel):
    idClientes: int
class MessageResponse(BaseModel):
    mensaje: str