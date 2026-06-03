from pydantic import BaseModel


class EventoBase(BaseModel):
    nombre: str
    descripcion: str | None = None


class EventoCreate(EventoBase):
    pass


class EventoResponse(EventoBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    mensaje: str