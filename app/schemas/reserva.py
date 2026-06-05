from datetime import date, datetime
from pydantic import BaseModel


class ReservaBase(BaseModel):
    idClientes: int
    fecha_evento: date
    hora_evento: str
    estado: str = "pendiente"
    total_reserva: float = 0


class ReservaCreate(ReservaBase):
    pass


class ReservaResponse(ReservaBase):
    id: int
    fecha_reserva: datetime | None = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    mensaje: str