from datetime import datetime
from pydantic import BaseModel


class PagoBase(BaseModel):
    idReservas: int
    monto_pagado: float
    metodo_pago: str
    estado: str = "pendiente"
    referencia: str | None = None


class PagoCreate(PagoBase):
    pass


class PagoResponse(PagoBase):
    id: int
    fecha_pago: datetime | None = None

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    mensaje: str