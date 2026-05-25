# AGENTS.md

## Contexto del proyecto

Este repositorio corresponde a un proyecto universitario llamado `ChatBot WhatsApp`.

El objetivo es construir un sistema de reservas de eventos por WhatsApp usando FastAPI y PostgreSQL, con integraciones futuras a WhatsApp Cloud API, OpenAI API, Google Forms y recordatorios automatizados.

## Flujo funcional esperado

1. El cliente escribe por WhatsApp.
2. El sistema responde automaticamente.
3. La IA consulta informacion de eventos, paquetes y reservas.
4. Si el cliente desea reservar, se le envia un formulario.
5. La reserva se registra en la base de datos.
6. Se gestionan pagos, recordatorios y seguimiento posterior.

## Decision tecnica actual

- El proyecto usa `SQL directo`, no ORM.
- Las consultas deben vivir en `repositories/`.
- La logica del negocio debe vivir en `services/`.
- Los endpoints deben vivir en `api/routes/`.
- `main.py` solo debe arrancar FastAPI y registrar routers.

## Estructura deseada

```text
app/
├─ main.py
├─ api/
│  ├─ router.py
│  └─ routes/
├─ core/
│  ├─ config.py
│  └─ database.py
├─ repositories/
├─ schemas/
└─ services/
```

## Tablas principales de la BD

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

## Convenciones de trabajo

- Mantener arquitectura por capas.
- No colocar SQL dentro de `main.py` ni `api/routes/`.
- No introducir ORM a menos que el usuario lo pida explicitamente.
- Mantener nombres claros por modulo: `cliente`, `evento`, `reserva`, `pago`, etc.
- Crear un modulo a la vez y probarlo antes de continuar.

## Modulos sugeridos a implementar despues de clientes

1. `eventos`
2. `paquetes`
3. `reservas`
4. `pagos`
5. `formularios`
6. `recordatorios`
7. `mensajes_ia`
8. `whatsapp`
9. `openai`

## Notas para asistentes de codigo

- Priorizar cambios pequenos y ordenados.
- Respetar la estructura existente.
- Antes de mover codigo, verificar en que capa debe vivir realmente.
- Si se implementa un nuevo modulo, crear sus archivos en `routes`, `schemas`, `services` y `repositories`.
