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

### Conectividad Frontend ↔ Backend

| Vista | APIs que llama | Estado |
|-------|---------------|--------|
| login.html | `ApiUsuarios.login()` | ⚠️ Hardcodeado (admin@eventbot.pe / admin123) |
| dashboard.html | `ApiClientes`, `ApiEventos`, `ApiReservas`, `ApiPagos`, `ApiRecordatorios` | ✅ Clientes/Eventos/Reservas/Pagos OK. Recordatorios: stub |
| clientes.html | `ApiClientes.listar/crear/eliminar` | ✅ Funcional |
| eventos.html | `ApiEventos`, `ApiPaquetes` | ✅ Funcional |
| reservas.html | `ApiReservas`, `ApiPagos` | ✅ Funcional |
| pagos.html | `ApiPagos.listar/crear/actualizar` | ✅ Funcional |
| recordatorios.html | `ApiRecordatorios` | ❌ Stub (datos vacios) |
| conversaciones.html | `ApiClientes`, `ApiMensajes`, `POST /api/ia` | ❌ ApiMensajes es stub |
| reportes.html | `ApiReservas`, `ApiPagos`, `ApiClientes`, `ApiEventos` | ✅ Funcional |
| usuarios.html | `ApiUsuarios` | ❌ Stub (login hardcodeado) |

### Issues de Compatibilidad Conocidos
1. `api.js`: `ApiRecordatorios` y `ApiMensajes` son stubs (`async () => []`)
2. `api.js`: `ApiUsuarios.login()` no llama backend, usa credenciales hardcodeadas
3. Dashboard: espera `r.clienteNombre` pero backend devuelve `idClientes` (muestra "—")
4. Estados en frontend en mayuscula ("Confirmada") vs backend en minuscula ("confirmada")
5. Dashboard `ApiRecordatorios.listar()` es stub, no llama al endpoint real
6. `auth.js`: login hardcodeado en localStorage, no hay backend de usuarios

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

## Cambios de la Sesion Actual (03/07/2026)

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

## Pendientes / Proximos Pasos

- [x] Modulo `usuarios` backend (login real con JWT)
- [ ] Conectar `ApiRecordatorios` del frontend a los endpoints reales
- [ ] Conectar `ApiMensajes` del frontend (chat history)
- [x] Envio automatico de recordatorios (cron/scheduler)
- [ ] Encuesta de satisfaccion post-evento
- [ ] Arreglar field mismatches (clienteNombre, estados mayus/minus)
- [ ] Normalizar campo `nombre_paquete` en frontend (backend espera `nombre`)
- [ ] Bugs criticos pendientes: `password_hash` en `usuario_service._normalize()` ya corregido
- [ ] Bug: `ia_service.py` indices historial — corregido
- [ ] Bug: pagos 404 intermitentes — corregido (idempotente)
