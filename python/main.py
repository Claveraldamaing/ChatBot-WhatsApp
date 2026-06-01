from fastapi import FastAPI, Request, Query, Response, HTTPException
import requests
import time  # <--- 1. IMPORTANTE: Agregamos el módulo time aquí arriba para especificar el filtro de mensajes antiguos antes de que el bot envíe y reciba respuestas anitguas y no responda mensajes antiguos.

app = FastAPI()

# 1. Credenciales vinculadas con Meta Developers -Esta información es para que se pueda conectar el servidor con meta.ia developers-
VERIFY_TOKEN = "adonaiibuga" 
WHATSAPP_TOKEN = "EAAWATIXFnCEBRrsfUnq44vAGDfIVFJLjMXZAaOlLHCogVxiktq2nJq7UGRo5sUZAO1MxJ5ekfeD5iNdCQIGfNSMBUTdC4j3so3B8T81A3W1xpvyiIjmRUs25xbN0sSi6zfpG24TdnyOyIcAoV8iIbpUEtb8kxPHKEoZCmJDdDRMNFzuJ5t1RtjSECOIxyvQ9nbC4uTyBucCbpcFx9uOGIZAbJ77vwVKpYr0JiU37"
PHONE_NUMBER_ID = "1040672982473670"

@app.get("/webhook")
def verificar_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    # Meta hace una petición GET para validar la contraseña técnica del puente
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("✅ ¡Webhook verificado con éxito por Meta!")
        # Retornamos el challenge como texto plano puro (obligatorio para Meta)
        return Response(content=hub_challenge, media_type="text/plain")
    
    raise HTTPException(status_code=403, detail="Token de verificación inválido")

@app.post("/webhook")
async def recibir_mensaje(request: Request):
    data = await request.json()
    print("📥 Datos brutos recibidos de WhatsApp:", data)
    
    try:
        entry = data["entry"][0]["changes"][0]["value"]
        if "messages" in entry:
            mensaje = entry["messages"][0]
            telefono_cliente = mensaje["from"]
            texto_recibido = mensaje["text"]["body"]
            
            # --- 2. FILTRO ANTI-BUCLE (Agregado aquí) --- Para que no se reconozca el mensaje de los usuarios doble vez y esté respondiendo el servidor constamente.
            timestamp_mensaje = int(mensaje.get("timestamp", 0))
            tiempo_actual = int(time.time())
            
            # Si el mensaje es de hace más de 60 segundos, lo ignoramos donde específicamos por medio del 60s = 1 minuto.
            if (tiempo_actual - timestamp_mensaje) > 60:
                print(f"⚠️ Ignorando mensaje antiguo de {telefono_cliente}")
                return {"status": "ok"} 
            # --------------------------------------------

            print(f"\n📩 NUEVO MENSAJE DE: {telefono_cliente}")
            print(f"💬 CONTENIDO: {texto_recibido}")
            print("-" * 30)

            mensaje_bot = f"¡Hola! Recibí tu mensaje: '{texto_recibido}'. El ChatBot inteligente para la Atención y Gestión de Eventos está funcionando con éxito. 🚀"
            enviar_respuesta_whatsapp(telefono_cliente, mensaje_bot)
            
    except Exception as e:
        # Solo imprimimos si no es un mensaje (ej: confirmación de entrega)
        pass
        
    return {"status": "ok"} # SIEMPRE retorna esto al final de la función, para responder a meta siempre, evitando q el sistema reintente enviar el mismo mensaje.

def enviar_respuesta_whatsapp(to_number: str, message_text: str):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text}
    }
    response = requests.post(url, json=payload, headers=headers)
    print("📤 Respuesta de la API de Meta al enviar:", response.json())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)