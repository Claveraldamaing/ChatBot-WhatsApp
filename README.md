# ChatBot WhatsApp

Backend en FastAPI para un chatbot inteligente de reservas de eventos infantiles por WhatsApp.

## Objetivo

Automatizar la atencion al cliente, mostrar eventos y paquetes, registrar reservas, gestionar pagos y almacenar historial conversacional usando FastAPI, PostgreSQL y OpenAI.

## Flujo del proyecto

1. El cliente escribe al WhatsApp de la empresa.
2. El bridge local (`whatsapp-web.js`) recibe el mensaje y lo reenvia a FastAPI.
3. El sistema revisa si el numero existe en BD.
4. Si es **cliente nuevo** → el bot envia link de formulario de registro.
5. Si es **cliente existente** → IA responde o envia link de formulario de reserva.
6. Cuando se llena el formulario de reserva, se crea la reserva + detalle en BD.
7. El cliente paga y envia comprobante, el admin confirma el pago.
8. Se gestionan recordatorios y seguimiento posterior.

## Tecnologias

- FastAPI (Python)
- PostgreSQL (psycopg, sin ORM)
- OpenAI GPT-4o-mini
- whatsapp-web.js (Node.js)
- HTML/CSS/JS puro (formularios embebidos)

## Arquitectura por capas

```
app/
├── main.py                 # Arranque de FastAPI
├── api/
│   ├── router.py           # Registro de routers
│   └── routes/             # Endpoints HTTP (uno por modulo)
├── core/
│   ├── config.py           # Variables de entorno
│   └── database.py         # Conexion a PostgreSQL
├── repositories/           # Consultas SQL directo (SOLO AQUI)
├── schemas/                # Modelos Pydantic
├── services/               # Logica de negocio
└── templates/              # Formularios HTML
```

## Estructura actual del proyecto

```
ChatBot_WhatsApp/
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── router.py
│   │   └── routes/
│   │       ├── clientes.py
│   │       ├── eventos.py
│   │       ├── paquetes.py
│   │       ├── paquetes_eventos.py
│   │       ├── reservas.py
│   │       ├── detalle_reserva.py
│   │       ├── pagos.py
│   │       ├── ia.py
│   │       ├── whatsapp.py
│   │       └── formularios.py
│   ├── schemas/
│   │   ├── cliente.py
│   │   ├── evento.py
│   │   ├── paquete.py
│   │   ├── paquete_evento.py
│   │   ├── reserva.py
│   │   ├── detalle_reserva.py
│   │   ├── pago.py
│   │   └── ia.py
│   ├── services/
│   │   ├── cliente_service.py
│   │   ├── evento_service.py
│   │   ├── paquete_service.py
│   │   ├── paquete_evento_service.py
│   │   ├── reserva_service.py
│   │   ├── detalle_reserva_service.py
│   │   ├── pago_service.py
│   │   ├── ia_service.py
│   │   └── whatsapp_service.py
│   ├── repositories/
│   │   ├── cliente_repository.py
│   │   ├── evento_repository.py
│   │   ├── paquete_repository.py
│   │   ├── paquete_evento_repository.py
│   │   ├── reserva_repository.py
│   │   ├── detalle_reserva_repository.py
│   │   ├── pago_repository.py
│   │   └── mensajes_ia_repository.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   └── templates/
│       ├── formulario_clientes.html
│       └── formulario_reserva.html
├── whatsapp-bridge/
│   ├── bridge.js
│   └── package.json
├── docs/
│   ├── ACTUALIZACION_BRIDGE_LOCAL.md
│   └── BD.md
├── .env
├── .gitignore
├── requirements.txt
├── AGENTS.md
├── CONTEXTO_META.md
└── README.md
```

## Modulos implementados (9)

| Modulo | Route | Schema | Service | Repository | Estado |
|--------|-------|--------|---------|------------|--------|
| clientes | ✅ | ✅ | ✅ | ✅ | Completo |
| eventos | ✅ | ✅ | ✅ | ✅ | Completo |
| paquetes | ✅ | ✅ | ✅ | ✅ | Completo |
| paquetes_eventos | ✅ | ✅ | ✅ | ✅ | Completo |
| reservas | ✅ | ✅ | ✅ | ✅ | Completo |
| detalle_reserva | ✅ | ✅ | ✅ | ✅ | Completo |
| pagos | ✅ | ✅ | ✅ | ✅ | Basico |
| ia | ✅ | ✅ | ✅ | repo mensajes | Basico |
| whatsapp | ✅ | — | ✅ | — | Funcional |
| formularios | ✅ | — | — | — | Parcial |

## Endpoints disponibles

### API REST
- `GET /api/clientes`
- `GET /api/clientes/{id}`
- `POST /api/clientes`
- `PUT /api/clientes/{id}`
- `DELETE /api/clientes/{id}`
- `GET /api/eventos`
- `GET /api/eventos/{id}`
- `POST /api/eventos`
- `GET /api/paquetes`
- `GET /api/paquetes/{id}`
- `POST /api/paquetes`
- `GET /api/paquetes-eventos`
- `GET /api/eventos/{id}/paquetes`
- `POST /api/paquetes-eventos`
- `GET /api/reservas`
- `GET /api/reservas/{id}`
- `GET /api/clientes/{id}/reservas`
- `POST /api/reservas`
- `GET /api/detalle-reserva`
- `GET /api/detalle-reserva/{id}`
- `GET /api/reservas/{id}/detalle`
- `POST /api/detalle-reserva`
- `GET /api/pagos`
- `POST /api/pagos`
- `POST /api/ia`
- `POST /webhook-local`

### Formularios
- `GET /formulario/cliente?telefono=XXX`
- `GET /formulario/reserva?telefono=XXX`
- `POST /formulario/reserva`

## Base de datos

Base de datos PostgreSQL con 12 tablas. Documentacion completa en `docs/BD.md`.

| Tabla | Descripcion |
|-------|-------------|
| clientes | Datos de clientes |
| mensajes_ia | Historial de conversaciones con IA |
| eventos | Tipos de evento (Cumpleaños, Baby Shower) |
| paquetes | Paquetes disponibles (Basico, Premium, Hora Extra) |
| paquetes_eventos | Relacion muchos-a-muchos eventos-paquetes |
| reservas | Reservas realizadas por clientes |
| detalle_reserva | Items dentro de cada reserva |
| pagos | Pagos realizados (Yape, transferencia) |
| tipo_formulario | Tipos de formulario |
| formularios | Formularios enviados y respuestas |
| recordatorios | Recordatorios programados |
| usuarios | Usuarios del sistema (admin) |

## Como ejecutar el proyecto

**Terminal 1 — FastAPI:**
```bash
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Terminal 2 — Bridge WhatsApp (Node.js):**
```bash
cd whatsapp-bridge
node bridge.js
# Escanear QR con WhatsApp
```

**Acceder a la documentacion:**
```
http://127.0.0.1:8000/docs
```

## Variables de entorno (`.env`)

```env
DB_NAME=proyecto_chatbot
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
OPENAI_API_KEY=sk-...
NGROK_URL=https://tu-url.ngrok-free.dev
FORM_CLIENTE_URL=https://forms.gle/...     # Opcional
FORM_RESERVA_URL=https://forms.gle/...     # Opcional
```
