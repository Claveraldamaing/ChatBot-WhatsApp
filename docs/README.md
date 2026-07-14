# ChatBot WhatsApp

Backend FastAPI + Frontend HTML para chatbot inteligente de reservas de eventos infantiles por WhatsApp.

## Objetivo

Automatizar la atencion al cliente, mostrar eventos y paquetes, registrar reservas, gestionar pagos y almacenar historial conversacional usando FastAPI, PostgreSQL y OpenAI.

## Flujo del proyecto

1. El cliente escribe al WhatsApp de la empresa.
2. Bridge local (`whatsapp-web.js`) recibe el mensaje y lo reenvia a FastAPI.
3. Sistema revisa si el numero existe en BD.
4. Si es **cliente nuevo** → bot envia link de formulario de registro.
5. Si es **cliente existente** → IA responde o envia link de formulario de reserva.
6. Cuando se llena el formulario, se crea reserva + detalle + pago 50% pendiente.
7. Admin confirma pago → reserva pasa a "confirmada".
8. Al final del evento, se registra 2do pago 50% → reserva "completada".
9. Recordatorios automaticos: antes del evento, pago pendiente, post-evento.

## Tecnologias

- FastAPI (Python)
- PostgreSQL (psycopg, sin ORM)
- OpenAI GPT-4o-mini
- whatsapp-web.js (Node.js)
- HTML/CSS/JS puro (frontend + formularios)

## Estructura

```
ChatBot_WhatsApp/
├── app/                  # Backend FastAPI (13 modulos)
├── frontend/             # Panel admin (10 vistas)
├── whatsapp-bridge/      # Bridge Node.js
├── docs/                 # Documentacion
├── .env, AGENTS.md, README.md
```

### Modulos (13)

| Modulo | Route | Schema | Service | Repository |
|--------|-------|--------|---------|------------|
| clientes | ✅ | ✅ | ✅ | ✅ |
| eventos | ✅ | ✅ | ✅ | ✅ |
| paquetes | ✅ | ✅ | ✅ | ✅ |
| paquetes_eventos | ✅ | ✅ | ✅ | ✅ |
| reservas | ✅ | ✅ | ✅ | ✅ |
| detalle_reserva | ✅ | ✅ | ✅ | ✅ |
| pagos | ✅ | ✅ | ✅ | ✅ |
| recordatorios | ✅ | ✅ | ✅ | ✅ |
| mensajes_ia | ✅ | ✅ | ✅ | ✅ |
| usuarios | ✅ | ✅ | ✅ | ✅ |
| ia | ✅ | ✅ | ✅ | ✅ |
| whatsapp | ✅ | — | ✅ | — |
| formularios | ✅ | — | — | — |

### BD (10 tablas)

clientes, mensajes_ia, eventos, paquetes, paquetes_eventos, reservas, detalle_reserva, pagos, recordatorios, usuarios

## Como ejecutar

**Terminal 1 — FastAPI (backend + frontend):**
```bash
source venv/Scripts/activate && uvicorn app.main:app --reload
```

**Terminal 2 — Bridge WhatsApp (opcional):**
```bash
cd whatsapp-bridge && node bridge.js
```

**Panel admin:** `http://localhost:8000/views/login.html` (admin@eventbot.pe / admin123)
**API docs:** `http://localhost:8000/docs`
