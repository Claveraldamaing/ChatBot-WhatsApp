from pydantic import BaseModel


class PaqueteEventoBase(BaseModel):
    idPaquetes: int
    idEventos: int


class PaqueteEventoCreate(PaqueteEventoBase):
    pass


class PaqueteEventoResponse(PaqueteEventoBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    mensaje: str