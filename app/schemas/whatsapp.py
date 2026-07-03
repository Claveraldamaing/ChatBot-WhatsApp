from pydantic import BaseModel

class MensajeWebhook(BaseModel):
    telefono: str
    texto: str