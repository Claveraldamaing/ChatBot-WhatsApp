from fastapi import APIRouter
from app.schemas.whatsapp import MensajeWebhook
from app.services.whatsapp_service import WhatsAppService


router = APIRouter(tags=["whatsapp"])
service = WhatsAppService()
@router.post("/webhook-local")
async def webhook_local(mensaje: MensajeWebhook):
    try:
        respuesta = service.procesar_mensaje_local(mensaje.telefono, mensaje.texto)
        if respuesta:
            return {"status": "ok", "respuesta": respuesta}
    except Exception as e:
        print(f"[WHATSAPP] Error procesando mensaje: {e}")
    return {"status": "ok", "respuesta": "Lo siento, ocurrio un error. Intenta de nuevo."}