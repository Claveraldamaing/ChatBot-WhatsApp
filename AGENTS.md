# AGENTS.md

## Contexto del proyecto

Proyecto universitario (UCV - 8vo ciclo, Gestion de Proyectos) llamado ChatBot WhatsApp.
Sistema de reservas de eventos infantiles por WhatsApp usando FastAPI + PostgreSQL + OpenAI.

## Equipo (5 integrantes)

- **Clavoxx** — Limpieza del repo, mejora del bridge, coordinacion, testing final
- **Erick** — IA + Formularios + Flujo de registro y reserva de clientes
- **Patrick** — Frontend (panel admin con HTML/CSS/JS)
- **Jefferson** — Frontend (panel admin con HTML/CSS/JS)
- **Juan** — Recordatorios + Pagos

## Flujo funcional esperado

1. El cliente escribe por WhatsApp.
2. Bridge local recibe el mensaje y lo reenvia a FastAPI.
3. Sistema revisa si el numero existe en BD.
4. Si es cliente nuevo -> bot envia link de formulario de registro.
5. Si es cliente existente -> IA responde o envia link de formulario de reserva.
6. Cuando se llena el formulario, se crea la reserva + detalle + pago pendiente.
7. El cliente paga y envia comprobante, el admin confirma el pago.
8. Se gestionan recordatorios y seguimiento posterior.

## Stack tecnologico

- Backend: FastAPI (Python)
- Base de Datos: PostgreSQL con SQL directo (psycopg), sin ORM
- IA: OpenAI GPT-4o-mini
- Bridge WhatsApp: whatsapp-web.js (Node.js)
- Frontend: HTML/CSS/JS puro (sin frameworks)

## Arquitectura por capas

```
app/
├── main.py                 # Arranca FastAPI y registra routers
├── api/
│   ├── router.py           # Registro de todos los routers
│   └── routes/             # Endpoints HTTP (uno por modulo)
├── core/
│   ├── config.py           # Variables de entorno
│   └── database.py         # Conexion a PostgreSQL
├── repositories/           # Consultas SQL directo (SOLO AQUI)
├── schemas/                # Modelos Pydantic
└── services/               # Logica de negocio
```

## Convenciones de trabajo

- Mantener arquitectura por capas.
- SQL solo en repositories/.
- Logica de negocio solo en services/.
- Endpoints solo en api/routes/.
- main.py solo arranca FastAPI y registra routers.
- No usar ORM (SQLAlchemy esta instalado pero no se usa).
- Nombres claros por modulo: cliente, evento, reserva, pago, etc.
- Si se crea un modulo nuevo, crear sus 4 archivos: route, schema, service, repository.

## Tablas de la BD (12 tablas)

1. `clientes` - nombre, telefono, email, fecha_registro
2. `mensajes_ia` - historial de conversaciones con rol, contenido, tipo, estado
3. `eventos` - tipo de evento (nombre, descripcion)
4. `paquetes` - nombre, descripcion, precio, estado
5. `paquetes_eventos` - relacion evento-paquete (many-to-many)
6. `reservas` - idCliente, fecha_evento, hora_evento, estado, total
7. `detalle_reserva` - items de la reserva (cantidad, subtotal)
8. `pagos` - monto, metodo, estado, referencia
9. `tipo_formulario` - tipos de formulario (registro, reserva, satisfaccion)
10. `formularios` - formularios enviados (respuesta_json)
11. `recordatorios` - recordatorios programados (tipo, mensaje, fecha)
12. `usuarios` - login del sistema (nombre, email, password_hash, rol)

## Estado actual de modulos

### Completos (9)
- clientes, eventos, paquetes, paquetes_eventos
- reservas, detalle_reserva, pagos (basico)
- ia (basico), whatsapp (con bridge)

### En desarrollo / Pendientes
- frontend/ (panel admin) - Patrick + Jefferson
- formularios (routes, schema, service, repo) - Erick
- usuarios (routes, schema, service, repo) - Patrick + Jefferson
- recordatorios (routes, schema, service, repo) - Juan
- pagos (mejora: confirmar, pendientes, historial) - Juan
- ia_service.py (mejora: cliente nuevo vs existente, formularios) - Erick
