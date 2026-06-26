from fastapi import APIRouter
from app.services.whatsapp_service import WhatsAppService
from pydantic import BaseModel
router = APIRouter(tags=["whatsapp"])
service = WhatsAppService()
class MensajeLocal(BaseModel):
    telefono: str
    texto: str
    
@router.post("/webhook-local")
async def webhook_local(mensaje: MensajeLocal):
    respuesta = service.procesar_mensaje_local(mensaje.telefono, mensaje.texto)
    if respuesta:
        return {"status": "ok", "respuesta": respuesta}
    return {"status": "error", "respuesta": "No se pudo procesar"}