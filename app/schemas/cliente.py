from datetime import datetime

from pydantic import BaseModel


class ClienteBase(BaseModel):
    nombre: str
    telefono: str
    email: str| None = None


class ClienteCreate(ClienteBase):
    lid: str | None = None


class ClienteResponse(ClienteBase):
    id: int
    fecha_registro: datetime | None = None


class MessageResponse(BaseModel):
    mensaje: str
