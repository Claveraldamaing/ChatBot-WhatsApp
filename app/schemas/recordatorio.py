from datetime import datetime
from pydantic import BaseModel
class RecordatorioBase(BaseModel):
    idReservas: int
    tipo: str
    mensaje: str
    fecha_programada: datetime
    estado: str = "pendiente"
class RecordatorioCreate(RecordatorioBase):
    pass
class RecordatorioResponse(RecordatorioBase):
    id: int
    fecha_envio: datetime | None = None
    class Config:
        from_attributes = True
class MessageResponse(BaseModel):
    mensaje: str