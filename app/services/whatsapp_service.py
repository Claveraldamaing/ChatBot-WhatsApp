import time
import requests
from app.core.config import settings
from app.schemas.whatsapp import WebhookPayload

class WhatsAppService:

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