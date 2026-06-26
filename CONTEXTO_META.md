# Contexto del Proyecto - ChatBot WhatsApp

## Que es este proyecto
Backend universitario (UCV - 8vo ciclo, Gestion de Proyectos) para un chatbot inteligente de reservas de eventos infantiles por WhatsApp usando FastAPI + PostgreSQL + OpenAI.

## Integrantes del equipo (5)
- **Clavoxx** (dueño del repo) — Limpieza, Bridge, Coordinacion general
- **Erick** — IA, Formularios, Flujo de registro y reserva de clientes
- **Patrick** — Frontend (panel admin)
- **Jefferson** — Frontend (panel admin)
- **Juan** — Recordatorios y Pagos

## Arquitectura del proyecto
```
ChatBot_WhatsApp/
├── app/                          # Backend FastAPI
│   ├── main.py                   # Punto de entrada FastAPI
│   ├── api/
│   │   ├── router.py             # Registro de routers
│   │   └── routes/               # Endpoints HTTP
│   │       ├── clientes.py       # CRUD clientes
│   │       ├── eventos.py        # CRUD eventos
│   │       ├── paquetes.py       # CRUD paquetes
│   │       ├── paquetes_eventos.py # Relacion paquete-evento
│   │       ├── reservas.py       # CRUD reservas
│   │       ├── detalle_reserva.py # CRUD detalle reserva
│   │       ├── pagos.py          # CRUD pagos
│   │       ├── ia.py             # Endpoint de IA
│   │       └── whatsapp.py       # Webhook Meta + endpoint local
│   ├── schemas/                  # Modelos Pydantic
│   ├── services/
│   │   ├── ia_service.py         # Logica OpenAI
│   │   └── whatsapp_service.py   # Servicio de WhatsApp
│   ├── repositories/             # SQL directo (sin ORM)
│   │   ├── cliente_repository.py
│   │   ├── evento_repository.py
│   │   ├── paquete_repository.py
│   │   ├── paquete_evento_repository.py
│   │   ├── reserva_repository.py
│   │   ├── detalle_reserva_repository.py
│   │   ├── pago_repository.py
│   │   └── mensajes_ia_repository.py
│   └── core/
│       ├── config.py             # Variables de entorno
│       └── database.py           # Conexion a PostgreSQL
├── frontend/                     # Panel admin (Patrick + Jefferson)
├── whatsapp-bridge/              # Bridge local (Node.js)
│   ├── package.json
│   └── bridge.js                 # whatsapp-web.js, escucha QR
├── docs/
│   └── ACTUALIZACION_BRIDGE_LOCAL.md
├── CONTEXTO_META.md
└── AGENTS.md
```

## Estado actual del proyecto (Junio 2026)
- 9 modulos backend implementados (clientes, eventos, paquetes, paquetes_eventos, reservas, detalle_reserva, pagos, ia, whatsapp) ✅
- Bridge local (`whatsapp-web.js`) implementado y conectado ✅
- Flujo completo: mensaje WhatsApp → bridge → FastAPI → IA → respuesta ✅
- Solo responde a numeros NO guardados en contactos (no interfiere con uso personal) ✅
- BD PostgreSQL con 12 tablas y datos de prueba ✅

## Modulos pendientes (en desarrollo)
- Frontend (panel admin) — Patrick + Jefferson
- Formularios (repo, service, route, schema) — Erick
- Usuarios (login para el panel) — Patrick + Jefferson
- Recordatorios (completo) — Juan
- Pagos (mejora: confirmar, pendientes) — Juan
- IA mejorada (flujo cliente nuevo vs existente, formularios) — Erick



## Base de Datos (PostgreSQL)
12 tablas en `creacion_bd.sql`:
1. `clientes` - Datos de clientes (nombre, telefono, email)
2. `mensajes_ia` - Historial de conversaciones con la IA
3. `eventos` - Tipos de evento (Cumpleanos, Baby Shower)
4. `paquetes` - Paquetes (Basico S/300, Premium S/500, Hora Extra S/80)
5. `paquetes_eventos` - Relacion muchos-a-muchos entre eventos y paquetes
6. `reservas` - Reservas hechas por clientes
7. `detalle_reserva` - Items dentro de cada reserva
8. `pagos` - Pagos realizados (Yape, transferencia)
9. `tipo_formulario` - Tipos de formularios
10. `formularios` - Formularios enviados y sus respuestas
11. `recordatorios` - Recordatorios programados
12. `usuarios` - Usuarios del sistema (admin)

## Como levantar el proyecto

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

**Terminal 3 — Frontend (opcional):**
```bash
# Abrir frontend/login.html en el navegador
# O usar Live Server de VS Code
```

Luego abrir `http://127.0.0.1:8000/docs`
