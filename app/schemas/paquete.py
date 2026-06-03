from pydantic import BaseModel


class PaqueteBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    estado: str="activo"


class PaqueteCreate(PaqueteBase):
    pass


class PaqueteResponse(PaqueteBase):
    id: int

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    mensaje: str