# Actualizacion: Bridge Local WhatsApp + whatsapp-web.js

## Fecha
Junio 2026

## Problema
La cuenta de Meta Business ("Show Infantiles") fue restringida, bloqueando el uso del webhook oficial de WhatsApp Cloud API para conectarse con el backend FastAPI.

## Solucion implementada
Se reemplazo la conexion via webhook de Meta por un **bridge local** usando `whatsapp-web.js` (Node.js) que se conecta directamente al WhatsApp personal del dueno mediante escaneo de codigo QR.

## Cambios realizados

### 1. Nueva carpeta: `whatsapp-bridge/`
Contiene el bridge en Node.js que se encarga de:
- Conectarse a WhatsApp via QR (sesion persistente con LocalAuth)
- Escuchar mensajes entrantes
- Filtrar mensajes de grupos y transmisiones
- **Ignorar mensajes de contactos guardados** (solo responde a numeros desconocidos)
- Enviar el mensaje a FastAPI via `POST /webhook-local`
- Recibir la respuesta de la IA y reenviarla por WhatsApp

Archivos:
- `package.json` — dependencias: whatsapp-web.js, qrcode-terminal, axios
- `bridge.js` — logica principal del bridge

### 2. Archivo modificado: `app/repositories/cliente_repository.py`
Se agregaron 2 metodos nuevos:
- `get_by_telefono(telefono)` — busca un cliente por numero de telefono
- `create_simple(telefono)` — crea un cliente nuevo solo con telefono (nombre generico "Cliente {telefono}"), devuelve el ID generado

### 3. Archivo modificado: `app/services/whatsapp_service.py`
- Se agrego importacion de `IAService` y `ClienteRepository`
- Se modifico `__init__` para inicializar `self.ia_service` y `self.cliente_repo`
- Se agrego metodo `procesar_mensaje_local(telefono, texto)` que:
  1. Busca el cliente por telefono en BD
  2. Si no existe, lo crea
  3. Llama a `IAService.responder()` con el texto y el ID de cliente
  4. Retorna la respuesta generada por OpenAI

### 4. Archivo modificado: `app/api/routes/whatsapp.py`
- Se agrego el schema `MensajeLocal` (telefono, texto)
- Se agrego endpoint `POST /webhook-local` que recibe mensajes del bridge, los procesa y envia la respuesta

### 5. Archivo modificado: `.gitignore`
Se agregaron lineas para ignorar:
- `whatsapp-bridge/node_modules/`
- `whatsapp-bridge/.wwebjs_auth/`

## Arquitectura resultante

```
WhatsApp (celular del cliente)
    ↓ mensaje
whatsapp-bridge (Node.js) — escucha localmente
    ↓ POST /webhook-local
FastAPI (app.main)
    ↓
ClienteRepository — busca o crea cliente por telefono
    ↓
IAService.responder() — OpenAI + historial + BD
    ↓
Respuesta → bridge → WhatsApp del cliente
```

## Como ejecutar

**Terminal 1 — FastAPI:**
```bash
venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

**Terminal 2 — Bridge:**
```bash
cd whatsapp-bridge
node bridge.js
```

Escanea el QR con WhatsApp. El bot respondera solo a numeros no guardados en la agenda.

## Estado
- FastAPI funcional ✅
- Bridge conectado a WhatsApp ✅
- Flujo completo: mensaje → IA → respuesta ✅
- Pendiente: integrar Google Forms para registro de clientes
