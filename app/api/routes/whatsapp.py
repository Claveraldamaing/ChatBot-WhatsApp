from fastapi import APIRouter, Query, Response, HTTPException
from app.schemas.whatsapp import WebhookPayload
from app.services.whatsapp_service import WhatsAppService
from pydantic import BaseModel


router = APIRouter(tags=["whatsapp"])
service = WhatsAppService()

@router.get("/webhook")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and service.verificar_token(hub_verify_token):
        print("Webhook verificado con exito por Meta!")
        return Response(content=hub_challenge, media_type="text/plain")
    raise HTTPException(status_code=403, detail="Token de verificacion invalido")

@router.post("/webhook")
async def recibir_mensaje(payload: WebhookPayload):
    resultado = service.procesar_mensaje(payload)
    if resultado:
        texto = f"Hola! Recibi tu mensaje: '{resultado['texto']}'. El ChatBot esta funcionando."
        service.enviar_respuesta(resultado["telefono"], texto)
    return {"status": "ok"}

class MensajeLocal(BaseModel):
    telefono: str
    texto: str
    
@router.post("/webhook-local")
async def webhook_local(mensaje: MensajeLocal):
    respuesta = service.procesar_mensaje_local(mensaje.telefono, mensaje.texto)
    if respuesta:
        service.enviar_respuesta(mensaje.telefono, respuesta)
        return {"status": "ok", "respuesta": respuesta}
    return {"status": "error", "respuesta": "No se pudo procesar"}