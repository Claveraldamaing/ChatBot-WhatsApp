from pydantic import BaseModel


class MensajeIA(BaseModel):
    idClientes: int
    texto: str


class RespuestaIA(BaseModel):
    idClientes: int
    mensaje_recibido: str
    respuesta_ia: str