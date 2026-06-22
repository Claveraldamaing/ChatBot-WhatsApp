import time
import requests
from app.services.ia_service import IAService
from app.repositories.cliente_repository import ClienteRepository
from app.core.config import settings
from app.schemas.whatsapp import WebhookPayload

class WhatsAppService:

    def __init__(self):
        self.ia_service = IAService()
        self.cliente_repo = ClienteRepository()

    def verificar_token(self, hub_verify_token: str) -> bool:
        return hub_verify_token == settings.verify_token
    
    def procesar_mensaje(self, payload: WebhookPayload) -> dict | None:
        try:
            value = payload.entry[0].changes[0].value
            if not value.messages:
                return None
            mensaje = value.messages[0]
            telefono = mensaje.from_
            texto = mensaje.text.body if mensaje.text else ""
            timestamp = int(mensaje.timestamp)
            ahora = int(time.time())
            if (ahora - timestamp) > 60:
                print(f"Ignorando mensaje antiguo de {telefono}")
                return None
            print(f"\nNUEVO MENSAJE DE: {telefono}")
            print(f"CONTENIDO: {texto}\n")
            return {"telefono": telefono, "texto": texto}
        except Exception as e:
            print(f"Error procesando mensaje: {e}")
            return None
        
    def procesar_mensaje_local(self, telefono: str, texto: str) -> str | None:
        cliente = self.cliente_repo.get_by_telefono(telefono)
        if cliente:
            id_clientes = cliente[0]
            print(f"Cliente existente: ID {id_clientes}")
        else:
            id_clientes = self.cliente_repo.create_simple(telefono)
            print(f"Nuevo cliente creado con ID: {id_clientes}")
        respuesta_ia = self.ia_service.responder(texto, id_clientes)
        return respuesta_ia
            
    def enviar_respuesta(self, to_number: str, message_text: str):
        url = f"https://graph.facebook.com/v18.0/{settings.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {settings.whatsapp_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message_text}
        }
        response = requests.post(url, json=payload, headers=headers)
        print("Respuesta de Meta:", response.json())