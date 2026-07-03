from fastapi import APIRouter
from app.schemas.whatsapp import MensajeWebhook
from app.services.whatsapp_service import WhatsAppService


router = APIRouter(tags=["whatsapp"])
service = WhatsAppService()
@router.post("/webhook-local")
async def webhook_local(mensaje: MensajeWebhook):
    respuesta = service.procesar_mensaje_local(mensaje.telefono, mensaje.texto)
    if respuesta:
        return {"status": "ok", "respuesta": respuesta}
    return {"status": "error", "respuesta": "No se pudo procesar"}