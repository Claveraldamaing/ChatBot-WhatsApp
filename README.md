# ChatBot WhatsApp

Backend en FastAPI para un chatbot inteligente de reservas de eventos por WhatsApp.

## Objetivo

Automatizar la atencion al cliente, mostrar eventos y paquetes, registrar reservas, gestionar pagos y almacenar historial conversacional usando FastAPI, PostgreSQL y OpenAI.

## Flujo del proyecto

1. El cliente escribe al WhatsApp de la empresa.
2. El chatbot responde automaticamente con informacion de eventos y paquetes.
3. La IA responde dudas usando informacion guardada en la base de datos.
4. Cuando el cliente desea reservar, se le envia un Google Forms.
5. La reserva se registra en PostgreSQL.
6. El sistema calcula total, registra pagos y envia recordatorios.
7. Despues del evento, se envia un formulario de satisfaccion.

## Tecnologias

- FastAPI
- PostgreSQL
- psycopg
- Python
- OpenAI API
- Google Forms

## Estructura actual

```text
app/
├─ main.py
├─ api/
│  ├─ router.py
│  └─ routes/
│     └─ clientes.py
├─ core/
│  ├─ config.py
│  └─ database.py
├─ repositories/
│  └─ cliente_repository.py
├─ schemas/
│  └─ cliente.py
└─ services/
   └─ cliente_service.py
```

## Arquitectura

El proyecto usa arquitectura por capas:

- `main.py`: arranque de la aplicacion
- `api/routes/`: endpoints HTTP
- `schemas/`: validacion de entrada y salida
- `services/`: logica del negocio
- `repositories/`: consultas SQL
- `core/`: configuracion y conexion a BD

## Base de datos

La base de datos del proyecto contempla estas tablas:

- `clientes`
- `mensajes_ia`
- `eventos`
- `paquetes`
- `paquetes_eventos`
- `reservas`
- `detalle_reserva`
- `pagos`
- `tipo_formulario`
- `formularios`
- `recordatorios`
- `usuarios`

## Modulo actual

Actualmente esta implementado el modulo `clientes` con rutas CRUD.

Endpoints disponibles:

- `GET /api/clientes`
- `GET /api/clientes/{cliente_id}`
- `POST /api/clientes`
- `PUT /api/clientes/{cliente_id}`
- `DELETE /api/clientes/{cliente_id}`

## Como ejecutar el proyecto

1. Activar el entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Levantar el servidor:

```bash
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

4. Abrir la documentacion:

```text
http://127.0.0.1:8000/docs
```

## Variables de entorno recomendadas

Crear un archivo `.env` con valores como estos:

```env
DB_NAME=proyecto_chatbot
DB_USER=postgres
DB_PASSWORD=12345
DB_HOST=localhost
DB_PORT=5432
```

## Estado del proyecto

Este proyecto esta en fase inicial. Ya se ordeno la estructura base en FastAPI y el siguiente paso es implementar los modulos de `eventos`, `paquetes` y `reservas`.
