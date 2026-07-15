# AGENTS.md — Contexto Completo del Proyecto

## ChatBot WhatsApp — Reservas de Eventos Infantiles

Proyecto universitario (UCV - 8vo ciclo, Gestion de Proyectos). Sistema de reservas de eventos infantiles por WhatsApp usando FastAPI + PostgreSQL + OpenAI GPT-4o-mini.

---


## Stack Tecnologico

- **Backend:** FastAPI (Python 3.12+)
- **Base de Datos:** PostgreSQL con SQL directo (psycopg2), sin ORM
- **IA:** OpenAI GPT-4o-mini
- **Bridge WhatsApp:** whatsapp-web.js (Node.js + Puppeteer)
- **Frontend:** HTML/CSS/JS puro (sin frameworks)

---

## Arquitectura por Capas

```
app/
├── main.py                 # Bootstrap FastAPI + CORS + StaticFiles
├── api/
│   ├── router.py           # Registro de todos los routers
│   └── routes/             # Endpoints HTTP (uno por modulo)
├── core/
│   ├── config.py           # Variables de entorno
│   └── database.py         # Conexion PostgreSQL (psycopg2)
├── repositories/           # Solo consultas SQL (NUNCA logica)
├── schemas/                # Modelos Pydantic
├── services/               # Logica de negocio
└── templates/              # Formularios HTML embebidos
```

--- 

## Estructura Completa del Proyecto

```
ChatBot_WhatsApp/
├── .env                          # Variables de entorno
├── .gitignore
├── AGENTS.md                     # ← ESTE ARCHIVO
├── README.md                     # Documentacion general
├── requirements.txt              # Dependencias Python
│
├── app/
│   ├── main.py                   # FastAPI: CORS + routers + StaticFiles + scheduler
│   ├── api/
│   │   ├── router.py             # Include de todos los routers (13 modulos)
│   │   └── routes/
│   │       ├── clientes.py       # CRUD clientes
│   │       ├── eventos.py        # CRUD eventos
│   │       ├── paquetes.py       # CRUD paquetes
│   │       ├── paquetes_eventos.py
│   │       ├── reservas.py       # CRUD + finalizar-pago
│   │       ├── detalle_reserva.py
│   │       ├── pagos.py          # CRUD + confirmar-pago (idempotente)
│   │       ├── recordatorios.py  # CRUD + generar-para-reserva + pendientes-para-enviar
│   │       ├── ia.py             # Consultar IA
│   │       ├── whatsapp.py       # Webhook local /webhook-local
│   │       ├── formularios.py    # Formularios HTML
│   │       ├── usuarios.py       # CRUD + auth/login JWT
│   │       └── mensajes_ia.py    # Listar/eliminar historial
│   ├── schemas/
│   │   ├── cliente.py
│   │   ├── evento.py
│   │   ├── paquete.py
│   │   ├── paquete_evento.py
│   │   ├── reserva.py
│   │   ├── detalle_reserva.py
│   │   ├── pago.py
│   │   ├── recordatorio.py
│   │   ├── ia.py
│   │   ├── mensaje_ia.py
│   │   ├── usuario.py
│   │   └── whatsapp.py
│   ├── services/
│   │   ├── cliente_service.py
│   │   ├── evento_service.py
│   │   ├── paquete_service.py
│   │   ├── paquete_evento_service.py
│   │   ├── reserva_service.py
│   │   ├── detalle_reserva_service.py
│   │   ├── pago_service.py
│   │   ├── recordatorio_service.py
│   │   ├── ia_service.py
│   │   ├── whatsapp_service.py
│   │   ├── mensajes_ia_service.py
│   │   └── usuario_service.py
│   ├── repositories/
│   │   ├── cliente_repository.py
│   │   ├── evento_repository.py
│   │   ├── paquete_repository.py
│   │   ├── paquete_evento_repository.py
│   │   ├── reserva_repository.py
│   │   ├── detalle_reserva_repository.py
│   │   ├── pago_repository.py
│   │   ├── recordatorio_repository.py
│   │   ├── mensajes_ia_repository.py
│   │   └── usuario_repository.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py          # ConnectionPool psycopg
│   │   └── scheduler.py         # APScheduler: recordatorios automaticos
│   └── templates/
│       ├── formulario_clientes.html
│       └── formulario_reserva.html
│
├── frontend/
│   ├── css/
│   │   └── eventbot.css
│   ├── js/
│   │   ├── api.js            # Cliente fetch → FastAPI
│   │   ├── auth.js           # Auth con localStorage
│   │   └── sidebar.js        # Componente sidebar
│   └── views/
│       ├── login.html        # Entry point (admin@eventbot.pe / admin123)
│       ├── dashboard.html
│       ├── clientes.html
│       ├── eventos.html
│       ├── reservas.html
│       ├── pagos.html
│       ├── recordatorios.html
│       ├── conversaciones.html
│       ├── reportes.html
│       └── usuarios.html
│
├── docs/
│   ├── AGENTS.md              # ← ESTE ARCHIVO
│   ├── README.md              # Documentacion general
│   └── BD.md                  # Documentacion de base de datos
│
└── whatsapp-bridge/
    ├── bridge.js             # whatsapp-web.js (Node.js)
    ├── package.json
    └── package-lock.json
```

---

## Base de Datos (10 tablas)

### Diagrama de Relaciones

```
clientes ──── mensajes_ia
    │
    └──── reservas ──── detalle_reserva ──── paquetes_eventos ──── eventos
              │                                           └──── paquetes
              ├──── pagos
              └──── recordatorios

usuarios (independiente)
```

### Tablas

#### 1. `clientes`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idClientes | SERIAL | PK |
| nombre | VARCHAR(100) | NOT NULL |
| telefono | VARCHAR(20) | NOT NULL, UNIQUE |
| email | VARCHAR(100) | |
| fecha_registro | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

#### 2. `mensajes_ia`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idMensajes_ia | SERIAL | PK |
| idClientes | INT | NOT NULL, FK → clientes |
| rol | VARCHAR(20) | NOT NULL ('cliente'/'asistente') |
| contenido | TEXT | NOT NULL |
| tipo | VARCHAR(30) | ('entrada'/'respuesta'/'texto') |
| fecha_hora_mensaje | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| estado | VARCHAR(30) | ('activo'/'recibido'/'enviado') |
| tiene_reserva | BOOLEAN | DEFAULT FALSE |

#### 3. `eventos`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idEventos | SERIAL | PK |
| nombre | VARCHAR(100) | NOT NULL |
| descripcion | TEXT | |

#### 4. `paquetes`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idPaquetes | SERIAL | PK |
| nombre_paquete | VARCHAR(100) | NOT NULL |
| descripcion | TEXT | |
| precio | NUMERIC(10,2) | NOT NULL |
| estado | VARCHAR(30) | DEFAULT 'activo' |

#### 5. `paquetes_eventos`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idPaquetesEventos | SERIAL | PK |
| idEventos | INT | NOT NULL, FK → eventos |
| idPaquetes | INT | NOT NULL, FK → paquetes |

#### 6. `reservas`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idReservas | SERIAL | PK |
| idClientes | INT | NOT NULL, FK → clientes |
| fecha_reserva | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| fecha_evento | DATE | NOT NULL |
| hora_evento | TIME | NOT NULL |
| estado | VARCHAR(30) | DEFAULT 'pendiente' |
| total_reserva | NUMERIC(10,2) | DEFAULT 0 |

**Estados:** `pendiente` → `confirmada` → `completada` | `cancelada`

#### 7. `detalle_reserva`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idDetalleReserva | SERIAL | PK |
| idReservas | INT | NOT NULL, FK → reservas |
| idPaquetesEventos | INT | NOT NULL, FK → paquetes_eventos |
| cantidad | INT | DEFAULT 1 |
| precio_unitario | NUMERIC(10,2) | NOT NULL |
| subtotal | NUMERIC(10,2) | NOT NULL |

#### 8. `pagos`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idPagos | SERIAL | PK |
| idReservas | INT | NOT NULL, FK → reservas |
| monto_pagado | NUMERIC(10,2) | NOT NULL |
| metodo_pago | VARCHAR(50) | NOT NULL ('Yape'/'Transferencia'/'Efectivo') |
| estado | VARCHAR(30) | DEFAULT 'pendiente' |
| fecha_pago | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| referencia | VARCHAR(100) | |

**Flujo de pagos:** 50% adelanto (confirma reserva) + 50% al final (completa reserva)

#### 9. `recordatorios`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idRecordatorio | SERIAL | PK |
| idReservas | INT | NOT NULL, FK → reservas |
| tipo | VARCHAR(50) | NOT NULL |
| mensaje | TEXT | NOT NULL |
| fecha_programada | TIMESTAMP | NOT NULL |
| fecha_envio | TIMESTAMP | |
| estado | VARCHAR(30) | DEFAULT 'pendiente' |

**Tipos:** `antes_evento`, `pago_pendiente`, `post_evento`
**Estados:** `pendiente`, `enviado`, `cancelado`

#### 10. `usuarios`
| Columna | Tipo | Restricciones |
|---------|------|---------------|
| idUsuario | SERIAL | PK |
| nombre | VARCHAR(100) | NOT NULL |
| email | VARCHAR(100) | NOT NULL, UNIQUE |
| password_hash | TEXT | NOT NULL |
| rol | VARCHAR(30) | NOT NULL ('admin'/'supervisor') |
| estado | VARCHAR(30) | DEFAULT 'activo' |
| fecha_registro | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |

---

## API REST — 57 Endpoints

### Clientes
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/clientes` | Listar todos |
| GET | `/api/clientes/{id}` | Obtener uno |
| POST | `/api/clientes` | Crear |
| PUT | `/api/clientes/{id}` | Actualizar |
| DELETE | `/api/clientes/{id}` | Eliminar |

### Eventos
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/eventos` | Listar |
| GET | `/api/eventos/{id}` | Obtener |
| POST | `/api/eventos` | Crear |
| PUT | `/api/eventos/{id}` | Actualizar |
| DELETE | `/api/eventos/{id}` | Eliminar |

### Paquetes
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/paquetes` | Listar |
| GET | `/api/paquetes/{id}` | Obtener |
| POST | `/api/paquetes` | Crear |
| PUT | `/api/paquetes/{id}` | Actualizar |
| DELETE | `/api/paquetes/{id}` | Eliminar |

### Paquetes-Eventos
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/paquetes-eventos` | Listar |
| GET | `/api/paquetes-eventos/{id}` | Obtener |
| GET | `/api/eventos/{id}/paquetes` | Paquetes por evento |
| POST | `/api/paquetes-eventos` | Crear |
| DELETE | `/api/paquetes-eventos/{id}` | Eliminar |

### Reservas
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/reservas` | Listar |
| GET | `/api/reservas/{id}` | Obtener |
| GET | `/api/clientes/{id}/reservas` | Por cliente |
| POST | `/api/reservas` | Crear |
| PUT | `/api/reservas/{id}` | Actualizar |
| DELETE | `/api/reservas/{id}` | Eliminar |
| POST | `/api/reservas/{id}/finalizar-pago` | Completar pago (50%→100%) |

### Detalle Reserva
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/detalle-reserva` | Listar |
| GET | `/api/detalle-reserva/{id}` | Obtener |
| GET | `/api/reservas/{id}/detalle` | Por reserva |
| POST | `/api/detalle-reserva` | Crear |
| PUT | `/api/detalle-reserva/{id}` | Actualizar |
| DELETE | `/api/detalle-reserva/{id}` | Eliminar |

### Pagos
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/pagos` | Listar |
| GET | `/api/pagos/{id}` | Obtener |
| GET | `/api/reservas/{id}/pagos` | Por reserva |
| POST | `/api/pagos` | Crear |
| PUT | `/api/pagos/{id}` | Actualizar |
| DELETE | `/api/pagos/{id}` | Eliminar |
| PUT | `/api/pagos/{id}/confirmar` | Confirmar pago (50%, idempotente) |

### Recordatorios
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/recordatorios` | Listar |
| GET | `/api/recordatorios/pendientes-para-enviar` | Listar pendientes con telefono |
| GET | `/api/recordatorios/{id}` | Obtener |
| GET | `/api/reservas/{id}/recordatorios` | Por reserva |
| POST | `/api/recordatorios` | Crear |
| PUT | `/api/recordatorios/{id}` | Actualizar |
| DELETE | `/api/recordatorios/{id}` | Eliminar |
| POST | `/api/recordatorios/generar-para-reserva/{id}` | Auto-generar 3 recordatorios |

### IA
| Metodo | Ruta | Accion |
|--------|------|--------|
| POST | `/api/ia` | Consultar OpenAI |

### WhatsApp
| Metodo | Ruta | Accion |
|--------|------|--------|
| POST | `/webhook-local` | Webhook del bridge local |

### Formularios
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/formulario/cliente?telefono=X` | Formulario registro |
| GET | `/formulario/reserva?telefono=X` | Formulario reserva |
| POST | `/formulario/reserva` | Crear reserva desde form |

### Mensajes IA
| Metodo | Ruta | Accion |
|--------|------|--------|
| GET | `/api/clientes/{id}/mensajes` | Historial conversacion |
| DELETE | `/api/mensajes/{id}` | Eliminar mensaje |

### Usuarios
| Metodo | Ruta | Accion |
|--------|------|--------|
| POST | `/api/auth/login` | Login (JWT) |
| GET | `/api/usuarios` | Listar |
| GET | `/api/usuarios/{id}` | Obtener |
| POST | `/api/usuarios` | Crear |
| PUT | `/api/usuarios/{id}` | Actualizar |
| DELETE | `/api/usuarios/{id}` | Eliminar |

---

## Flujo Completo del Sistema

```
WhatsApp (celular del cliente)
    │
    ▼ mensaje
whatsapp-bridge/bridge.js (Node.js)
    │ Filtra: solo numeros NO guardados + keywords (evento, reser, show, precio...)
    │
    ▼ POST /webhook-local
FastAPI → whatsapp_service.py → ClienteRepository (buscar/crear por telefono)
    │                                    →
    ▼                                    │
IA Service (OpenAI GPT-4o-mini)  ←  contexto de BD (cliente, reservas,
    │                                   pagos, eventos, paquetes, historial)
    ▼ respuesta
bridge → WhatsApp del cliente
```

### Sub-flujo: Formularios
```
IA detecta intencion de reserva
    │
    ▼ envia link
Cliente abre /formulario/reserva?telefono=X
    │
    ▼ llena datos + selecciona paquete
POST /formulario/reserva → crea reserva + detalle + pago 50% pendiente
    │
    ▼
Admin confirma pago → PUT /api/pagos/{id}/confirmar → reserva pasa a "confirmada"
    │
    ▼ fin del evento
POST /api/reservas/{id}/finalizar-pago → crea 2do pago 50% → reserva "completada"
```

### Sub-flujo: Recordatorios (auto-generados)
```
POST /api/recordatorios/generar-para-reserva/{id}
    │
    ├── antes_evento  (1 dia antes: recordatorio de fecha/hora)
    ├── pago_pendiente (3 dias antes, SOLO si reserva esta "pendiente")
    └── post_evento    (1 dia despues: agradecimiento + encuesta)
```

---

## Frontend — Panel Admin

### Conectividad Frontend ↔ Backend (Actualizado 15/07/2026)

| Vista | APIs que llama | Estado |
|-------|---------------|--------|
| login.html | `ApiUsuarios.login()` → `POST /api/auth/login` | ✅ Login real con JWT + bcrypt |
| dashboard.html | `ApiClientes`, `ApiEventos`, `ApiReservas`, `ApiPagos`, `ApiRecordatorios` | ✅ Todo real. Charts dinamicos (donut + bar + progress) |
| clientes.html | `ApiClientes` (CRUD completo) | ✅ Funcional + modal Ver/Editar |
| eventos.html | `ApiEventos`, `ApiPaquetes` | ✅ Funcional + stat cards + search |
| reservas.html | `ApiReservas`, `ApiPagos` | ✅ Funcional + modal + filtro case-insensitive |
| pagos.html | `ApiPagos` (CRUD completo) | ✅ Funcional + confirmar pago |
| recordatorios.html | `ApiRecordatorios` (CRUD + generar + pendientes) | ✅ Funcional + badges + marcar enviado |
| conversaciones.html | `ApiClientes`, `ApiMensajes`, `POST /api/ia` | ✅ Clientes y Mensajes reales. Chat con CSS vars |
| reportes.html | `ApiReservas`, `ApiPagos`, `ApiClientes`, `ApiEventos` | ✅ Funcional + donut dinamico + Excel export |
| usuarios.html | `ApiUsuarios` (CRUD + filtros) | ✅ Funcional + badge dinamico por sesion |

### Estado de API Objects en `api.js` (15/07/2026)

| API Object | Metodos | Estado |
|---|---|---|
| `ApiClientes` | 5 | ✅ Todos reales |
| `ApiEventos` | 5 | ✅ Todos reales |
| `ApiReservas` | 7 | ✅ Todos reales |
| `ApiPagos` | 7 | ✅ Todos reales |
| `ApiPaquetes` | 5 | ✅ Todos reales |
| `ApiPaquetesEventos` | 4 | ✅ Todos reales |
| `ApiDetalleReserva` | 3 | ✅ Todos reales |
| `ApiRecordatorios` | 7 | ✅ Todos reales (listar, crear, actualizar, eliminar, generar, pendientes, marcarEnviado) |
| `ApiMensajes` | 3 | ⚠️ 2 reales, 1 stub (`estadisticas`) |
| `ApiUsuarios` | 4 | ✅ Todos reales (incluye login JWT) |
| `ApiFormularios` | 1 | ❌ Stub (pendiente backend) |
| `ApiStatus` | 1 | ✅ Real |

### Issues de Compatibilidad — RESUELTOS
1. ~~`api.js`: `ApiRecordatorios` y `ApiMensajes` son stubs~~ → ✅ RESUELTO (solo `estadisticas` queda como stub)
2. ~~`api.js`: `ApiUsuarios.login()` no llama backend~~ → ✅ RESUELTO (login JWT real)
3. ~~Dashboard: espera `r.clienteNombre`~~ → ✅ RESUELTO (usa `idClientes` con fallback)
4. ~~Estados en frontend en mayuscula vs backend en minuscula~~ → ✅ RESUELTO (`.toLowerCase()` en todos los filtros)
5. ~~Dashboard `ApiRecordatorios.listar()` es stub~~ → ✅ RESUELTO (llama endpoint real)
6. ~~`auth.js`: login hardcodeado~~ → ✅ RESUELTO (JWT real con 8h expiry + 20min inactividad)

### Como Acceder
1. Backend sirve el frontend en la raiz: `http://localhost:8000/views/login.html`
2. Credenciales demo: `admin@eventbot.pe` / `admin123`

---

## Variables de Entorno (.env)

```env
DB_NAME=proyecto_chatbot
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
OPENAI_API_KEY=sk-proj-...
NGROK_URL=https://tu-url.ngrok-free.dev
```

---

## Cambios de la Sesion 03/07/2026

### Backend — Modulos nuevos
1. **`usuarios`** modulo completo: schema + service + repository + router (CRUD + auth JWT). Login real con bcrypt + JWT.
2. **`mensajes_ia`** modulo completo: schema + service + repository + router (listar historial por cliente, eliminar mensajes).
3. **`scheduler.py`** — APScheduler para envio automatico de recordatorios cada 1 minuto.

### Backend — Bugfixes y mejoras
4. **`recordatorios.py`**: Arreglado ruta `pendientes-para-enviar` (antes daba 422 por conflicto con `{recordatorio_id}`). Movida antes de la ruta greedy.
5. **`pago_service.py`**: `confirmar_pago()` ahora es idempotente — si ya esta pagado retorna 200 en vez de 404.
6. **`reserva_service.py`**: `finalizar_pago()` ahora es idempotente — si ya esta completada retorna 200 en vez de 404.
7. **`ia_service.py`**: Corregido indices del historial (enviaba `idMensajes_ia: idClientes` en vez de `rol: contenido`).
8. **`usuario_service.py`**: `_normalize()` ya no incluye `password_hash` (causaba 500). `update_usuario()` ahora hashea la password correctamente.
9. **`usuario_repository.py`**: UPDATE ahora incluye `password_hash`.

### Backend — Infraestructura
10. **`database.py`**: ConnectionPool de psycopg (login/bg) con `init_pool()`.
11. **`main.py`**: Agregado `init_pool()` + `iniciar_scheduler()` en startup.

### Archivos nuevos (9)
- `app/api/routes/usuarios.py`, `app/api/routes/mensajes_ia.py`
- `app/schemas/usuario.py`, `app/schemas/mensaje_ia.py`, `app/schemas/whatsapp.py`
- `app/services/usuario_service.py`, `app/services/mensajes_ia_service.py`
- `app/repositories/usuario_repository.py`
- `app/core/scheduler.py`

### Archivos modificados (11)
- `app/api/router.py`, `app/main.py`, `app/core/database.py`
- `app/api/routes/recordatorios.py`, `app/api/routes/whatsapp.py`, `app/api/routes/formularios.py`
- `app/services/ia_service.py`, `app/services/pago_service.py`, `app/services/reserva_service.py`
- `app/repositories/mensajes_ia_repository.py`
- `requirements.txt`

---

## Cambios de la Sesion 15/07/2026

Sesion intensiva de bugfixes, mejoras UX y revision visual completa. Branch: `fix/criticos-5bugs`.

### Backend (5 fixes)

| # | Archivo | Cambio |
|---|---------|--------|
| 1 | `whatsapp-bridge/bridge.js` | Servidor HTTP en puerto 8001 con `POST /send` ({telefono, texto}) para envio real de WhatsApp. Soporte LID (Contactos no guardados). |
| 2 | `app/core/scheduler.py` | Envio real via `httpx.post(BRIDGE_URL, ...)` en vez de solo `print()`. |
| 3 | `app/services/reserva_service.py` | `create_reserva()` auto-genera 3 recordatorios al crear reserva. |
| 4 | `app/services/recordatorio_service.py` | Nuevo metodo `marcar_enviado(id)`. |
| 5 | `app/api/routes/recordatorios.py` | Nuevo endpoint `PATCH /recordatorios/{id}/enviar`. |
| 6 | `app/repositories/cliente_repository.py` | Busqueda telefonica flexible: 3 formatos (limpio, 9 digitos, con prefijo 51). |
| 7 | `app/api/routes/pagos.py` | Endpoint `PUT /pagos/{id}/confirmar` (idempotente). |

### Frontend — Bugs Criticos y Altos (Fixes #1-12)

| # | Severidad | Archivo | Problema → Solucion |
|---|-----------|---------|---------------------|
| CRIT-1 | Critico | `login.html` | Labels confusos → Textos corregidos ("Correo electronico", "Contrasena") |
| CRIT-2 | Critico | `api.js` | API_BASE hardcodeada → Configurable via `localStorage.getItem("api_base")` |
| HIGH-1 | Alto | `clientes.html`, `pagos.html`, `reservas.html` | Botones "Exportar" muertos → Eliminados |
| HIGH-2 | Alto | `reportes.html` | Boton PDF muerto → Eliminado |
| HIGH-3 | Alto | `reportes.html` | Exportar CSV generaba nada → Genera archivo real |
| HIGH-4 | Alto | `clientes.html`, `reservas.html` | Botones Ver/Editar sin accion → Abren modales con datos reales |
| HIGH-5 | Alto | `api.js` | XSS via `showToast(html)` → Ahora usa `textContent` |
| HIGH-6 | Alto | `eventbot.css` | Sin focus-visible → Estilos accesibilidad agregados |
| MED-1 | Medio | `recordatorios.html` | Labels tecnicos → Human-readable ("Antes del evento", "Pago pendiente") |
| MED-2 | Medio | `reservas.html` | PAGE_SIZE inconsistente (5 vs 10) → Unificado a 10 |
| MED-3 | Medio | `api.js` | Toast sin animacion salida → Clase `eb-toast--out` con `modalOut` keyframe |
| MED-4 | Medio | `api.js` | `formatDate` sin validar fechas invalidas → Validacion agregada |

### Frontend — UX General (Fixes #13-22)

| # | Archivo | Mejora |
|---|---------|--------|
| 13 | Todas las vistas | **Tablas invertidas** — registros mas nuevos primero (clientes, eventos, reservas, pagos, recordatorios, conversaciones, dashboard) |
| 14 | `dashboard.html` | **Rediseñado** — Eliminado "4.8/5" hardcodeado, chart donut real (conic-gradient), mini bar chart ingresos por mes, progress bar tasa confirmacion, bordes laterales coloreados en stat cards |
| 15 | `reportes.html` | Donut dinamico via JS, eliminado "4.8" hardcodeado, eliminado stub formularios |
| 16 | `clientes.html` | Eliminado stub "Mensajes IA" |
| 17 | `conversaciones.html` | Eliminados 2 stats que mostraban "No disponible" |
| 18 | `dashboard.html` | Ingresos por mes ahora muestra montos S/. (no cantidad reservas) |
| 19 | `dashboard.html` | Progress bar con guards `Array.isArray()` + `if (lista.length > 0)` |

### Frontend — Auditoria 72 Items (Items #20-27)

| # | Severidad | Archivo | Cambio |
|---|-----------|---------|--------|
| MED-5 | Medio | `auth.js` | Logout con `confirm()` dialog |
| MED-6 | Medio | `usuarios.html` | Filtros combinados (texto + rol dropdown) |
| MED-7 | Medio | `reservas.html` | Filtro estado case-insensitive (`.toLowerCase()`) |

### Frontend — 50 Fixes Visuales (FASE 1-3)

**FASE 1 — CSS (`eventbot.css`) — 140+ lineas nuevas:**

| # | Tipo | Cambio |
|---|------|--------|
| 1 | Responsive | `@media` queries: tablet (<1024px) sidebar colapsa a 60px, stats a 2-col, forms 1-col; mobile (<640px) sidebar oculto, stats 1-col, search bars stack |
| 2+31 | Animacion | `@keyframes shimmer` + `.eb-skeleton`, `.eb-skeleton-text`, `.eb-skeleton-title`, `.eb-skeleton-circle` |
| 3 | Interaccion | `.eb-btn-success:hover` — dark green bg + white text |
| 4 | Interaccion | `.eb-btn:disabled` — opacity 0.5, cursor not-allowed, pointer-events none |
| 5 | Interaccion | `.eb-modal-close:hover` — red background + red color |
| 6 | Animacion | `@keyframes modalOut` + `.eb-toast--out` |
| 26 | CSS var | Table hover usa `var(--bg)` en vez de `#F8FAFC` hardcoded |
| 28 | Form | `select.eb-input` — custom dropdown arrow SVG via `appearance: none` + `background-image` |
| 29 | Layout | `.eb-separator` para flecha en filtros reportes |
| 34 | Cross-browser | Firefox scrollbar — `scrollbar-width: thin; scrollbar-color` |
| 35+36 | Namespace | `.eb-api-status`, `.eb-dot` (compat con `.api-status`/`.dot`) |
| 43 | A11y | `@media (prefers-reduced-motion: reduce)` — desactiva animaciones |
| 45 | Interaccion | `.eb-btn:active { transform: scale(0.97); }` |
| 46 | Transicion | `.eb-input` transition incluye `background` |
| — | Nuevo | `.eb-chat-area`, `.eb-chat-input`, `.eb-conv-item` para conversaciones |
| — | Nuevo | `.eb-login-row`, `.eb-login-remember`, `.eb-login-forgot`, `.eb-login-demo` para login |
| — | Nuevo | `.eb-sidebar-logout` con hover red |

**FASE 2 — JS (`api.js`):**

| # | Cambio |
|---|--------|
| 41+42 | Toast sin `style.animation` inline — usa clase CSS `.eb-toast--out` |

**FASE 3 — HTML (10 archivos):**

| Archivo | Fixes aplicados |
|---------|----------------|
| `recordatorios.html` | #7+#20: badgeEstado usa `.eb-badge` system |
| `conversaciones.html` | #9: CSS var colors; #10: stats con `.eb-stat`; #21: client hover `.eb-conv-item`; #27: chat bubbles CSS vars; #38: chat height responsive `.eb-chat-area`; #39: SVG send icon; #48: card header |
| `dashboard.html` | #11: sin `border-left` stat cards; #12: purple→green; #13: `.eb-grid-3`; #47: `.eb-donut`; empty states con iconos |
| `clientes.html` | #14: `.eb-grid-2`; empty state con icono |
| `reservas.html` | #14: `.eb-grid-3`; #19: doble margin eliminado; #50: modal icon `.eb-stat-icon`; empty state |
| `pagos.html` | #14: `.eb-grid-3`; #22: "Sin acciones" eliminado; empty state |
| `usuarios.html` | #14: `.eb-grid-3`; #23: badge dinamico; empty state |
| `eventos.html` | #15: `.eb-search-bar`; #16: stat cards; #17+#18: edit buttons con texto; search/filter; empty states |
| `login.html` | #24: CSS classes; #25: reducido inline styles; #32: `href="#"`→`href="login.html"`; #33: demo box CSS |
| `reportes.html` | #30: Excel en filter bar; `.eb-separator` |
| `sidebar.js` | #40: SVG logout icon + `.eb-sidebar-logout` |

### Archivos modificados en sesion 15/07/2026

**Backend (4 archivos):**
- `whatsapp-bridge/bridge.js`
- `app/core/scheduler.py`
- `app/services/reserva_service.py`
- `app/services/recordatorio_service.py`
- `app/api/routes/recordatorios.py`
- `app/repositories/cliente_repository.py`
- `app/api/routes/pagos.py`

**Frontend (14 archivos):**
- `frontend/css/eventbot.css`
- `frontend/js/api.js`
- `frontend/js/auth.js`
- `frontend/js/sidebar.js`
- `frontend/views/login.html`
- `frontend/views/dashboard.html`
- `frontend/views/clientes.html`
- `frontend/views/eventos.html`
- `frontend/views/reservas.html`
- `frontend/views/pagos.html`
- `frontend/views/recordatorios.html`
- `frontend/views/conversaciones.html`
- `frontend/views/reportes.html`
- `frontend/views/usuarios.html`

### Dependencias instaladas
- `psycopg_pool` (ConnectionPool para PostgreSQL)
- `python-jose[cryptography]` (JWT)
- `apscheduler` (scheduler)
- `bcrypt` + `passlib` (hashing passwords)

---

## Como Ejecutar

**Terminal 1 — FastAPI:**
```bash
cd "C:/Users/ClavoxxDC/Desktop/UCV/8VO CICLO/GESTION_PROYECTOS/ChatBot_WhatsApp"
source venv/Scripts/activate
uvicorn app.main:app --reload
```

**Terminal 2 — Bridge WhatsApp (opcional):**
```bash
cd whatsapp-bridge
node bridge.js
# Escanear QR con WhatsApp
```

**Acceder a:**
- Panel admin: `http://localhost:8000/views/login.html`
- Documentacion API: `http://localhost:8000/docs`

---

## Pendientes / Proximos Pasos (Actualizado 15/07/2026)

### Completado ✅
- [x] Modulo `usuarios` backend (login real con JWT)
- [x] Conectar `ApiRecordatorios` del frontend a los endpoints reales
- [x] Envio automatico de recordatorios (cron/scheduler)
- [x] Envio real de WhatsApp via bridge HTTP (puerto 8001)
- [x] Auto-generacion de recordatorios al crear reserva
- [x] Marcar recordatorio enviado (PATCH endpoint + boton UI)
- [x] Login real con JWT (no hardcodeado)
- [x] Logout con confirm dialog
- [x] Filtros combinados en todas las vistas
- [x] Tablas con orden cronologico inverso (mas nuevos primero)
- [x] Dashboard rediseñado (donut chart, bar chart, progress bar)
- [x] Reportes: donut dinamico + Excel export real
- [x] Modales Ver/Editar funcionales (clientes, reservas, usuarios)
- [x] XSS fix (showToast con textContent)
- [x] focus-visible para accesibilidad
- [x] Responsive CSS (tablet + mobile breakpoints)
- [x] Skeleton/shimmer animations
- [x] Empty states con iconos en todas las vistas
- [x] Arreglo field mismatches (clienteNombre, estados mayus/minus)
- [x] Bugs criticos: password_hash, ia_service indices, pagos 404 intermitentes
- [x] 72 items de auditoria resueltos
- [x] 50 fixes visuales implementados

### Pendiente — Prioridad Alta 🔴
- [ ] **Encuesta de satisfaccion post-evento** — El recordatorio `post_evento` envia agradecimiento, pero no recolecta respuestas
- [ ] **Chat conversaciones en tiempo real** — Actualmente muestra historial pero no actualiza automaticamente (necesita polling o WebSocket)
- [ ] **Validacion de formularios** — Los forms de crear/editar no tienen validacion HTML5 completa (required, patterns, min/max)

### Pendiente — Prioridad Media 🟡
- [ ] **`ApiMensajes.estadisticas`** — Stub, necesita endpoint backend para metricas de chat
- [ ] **`ApiFormularios`** — Stub, backend no tiene CRUD de formularios (solo los embebidos)
- [ ] **Paginacion real en frontend** — Las tablas muestran 10 items pero no tienen botones Siguiente/Anterior
- [ ] **Busqueda en backend** — El search es solo frontend (filtra la lista cargada). Para datos grandes necesitaría endpoints con query param `?q=`
- [ ] **Fotos de perfil de usuario** — Solo muestra iniciales, no permite subir imagen
- [ ] **Gestion de sesiones** — No hay endpoint para listar/cerrar sesiones activas (solo expira por tiempo)

### Pendiente — Prioridad Baja 🟢
- [ ] **Dark mode** — CSS ya usa variables (`--bg`, `--text`, etc.) facilitando dark mode futuro
- [ ] **Notificaciones push** — Admin no recibe notificaciones cuando hay nueva reserva
- [ ] **Exportar PDF** — Solo hay Excel; PDF eliminado pero podria re-implementarse con jsPDF
- [ ] **Multi-idioma** — Todo en espanol, pero estructura permite i18n futuro
- [ ] **Tests** — No hay tests unitarios ni de integracion (ni backend ni frontend)
- [ ] **CI/CD** — No hay pipeline de integracion continua
- [ ] **Docker** — No hay Dockerfile ni docker-compose
- [ ] **Rate limiting** — No hay proteccion contra abuso de la API

### Pendiente — Backend Especifico
- [ ] **Endpoint formularios CRUD** — Los formularios son HTML embebidos, no tienen API REST
- [ ] **Migraciones de BD** — No hay sistema de migraciones (ALTER TABLE manual)
- [ ] **Logging estructurado** — Solo `print()`, falta `logging` con niveles
- [ ] **Health check** — No hay `GET /health` o `GET /ready`

### Estado del Sistema (15/07/2026)

```
┌─────────────────────────────────────────────────────┐
│                    SISTEMA COMPLETO                  │
├─────────────────────────────────────────────────────┤
│ Backend (FastAPI)          │ 59 archivos Python     │
│ Frontend (HTML/CSS/JS)     │ 14 archivos (11 HTML)  │
│ Bridge (Node.js)           │ 1 archivo bridge.js    │
│ Base de Datos              │ 10 tablas PostgreSQL   │
│ API Endpoints              │ 57 endpoints REST      │
│ API Objects (frontend)     │ 12 objetos, 11 reales  │
│ Vistas Admin               │ 10 vistas completas    │
├─────────────────────────────────────────────────────┤
│ Auth:     JWT real (bcrypt + 8h expiry)             │
│ WhatsApp: Bridge HTTP (puerto 8001) + httpx         │
│ Scheduler: APScheduler cada 1 minuto                │
│ Charts:   Donut (conic-gradient) + Bar + Progress   │
│ Responsive: Tablet (<1024px) + Mobile (<640px)      │
│ Accesibilidad: focus-visible + reduced-motion        │
└─────────────────────────────────────────────────────┘
```
