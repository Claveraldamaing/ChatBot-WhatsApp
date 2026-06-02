from pydantic import BaseModel


class MensajeIA(BaseModel):
    session_id: str
    texto: str


class RespuestaIA(BaseModel):
    session_id: str
    mensaje_recibido: str
    respuesta_ia: str