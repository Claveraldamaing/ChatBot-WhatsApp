# Contexto del Proyecto - ChatBot WhatsApp

## Que es este proyecto
Backend universitario (UCV - 8vo ciclo, Gestion de Proyectos) para un chatbot inteligente de reservas de eventos por WhatsApp usando FastAPI + PostgreSQL + OpenAI.

## Arquitectura (por capas)
```
ChatBot_WhatsApp/
├── app/
│   ├── main.py                  # Punto de entrada FastAPI
│   ├── api/
│   │   ├── router.py            # Registro de routers
│   │   └── routes/              # Endpoints HTTP
│   │       ├── clientes.py, eventos.py, paquetes.py, ...
│   │       └── whatsapp.py      # Webhook Meta + endpoint local
│   ├── schemas/
│   ├── services/
│   │   ├── ia_service.py        # Logica OpenAI
│   │   └── whatsapp_service.py  # Servicio de WhatsApp
│   ├── repositories/
│   │   └── cliente_repository.py  # get_by_telefono + create_simple
│   └── core/
├── whatsapp-bridge/             # Bridge local (Node.js)
│   ├── package.json
│   └── bridge.js                # whatsapp-web.js, escucha QR
├── docs/
│   └── ACTUALIZACION_BRIDGE_LOCAL.md
└── CONTEXTO_META.md
```

## Estado actual
- Webhook de WhatsApp migrado y funcional ✅
- Bridge local (`whatsapp-web.js`) implementado y conectado ✅
- Flujo completo: mensaje WhatsApp → bridge → FastAPI → IA → respuesta ✅
- Solo responde a numeros NO guardados en contactos (no interfiere con uso personal) ✅
- `ClienteRepository` con `get_by_telefono` y `create_simple` ✅
- Endpoint `POST /webhook-local` para recibir mensajes del bridge ✅
- Meta API `enviar_respuesta()` falla por cuenta restringida (irrelevante, bridge responde)

## Problema con Meta Business
- Cuenta "Show Infantiles" restringida por "violacion de terminos"
- No se puede usar el webhook oficial
- Solucion temporal: bridge local con whatsapp-web.js

## Soluciones pendientes para webhook oficial
1. Apelar la restriccion
2. Pedir al companero que agregue como admin a su app
3. Bridge local funciona para testing/presentacion

## Como levantar el proyecto (para desarrollo local)

**Terminal 1 — FastAPI:**
```bash
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Terminal 2 — Bridge WhatsApp:**
```bash
cd whatsapp-bridge
node bridge.js
# Escanear QR con WhatsApp
```

Luego abrir `http://127.0.0.1:8000/docs`

## ngrok (solo si se recupera cuenta Meta)
- Instalado en `Instalador ngrok/`
- `ngrok http 8000`
- URL tipo `https://xxxx.ngrok-free.dev` + `/webhook`
- Verify Token: `adonaiibuga`
