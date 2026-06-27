# Bugs por arreglar — Dia 27/06/2026

## 🔴 Criticos (Afectan funcionamiento)

### Bug 1 — `whatsapp_service.py` linea 1: `import time` sin uso
**Archivo:** `app/services/whatsapp_service.py`
**Accion:** Eliminar `import time` de la linea 1.
```python
# Eliminar esta linea:
import time
```

### Bug 2 — Formulario de reserva no valida seleccion de paquete
**Archivo:** `app/templates/formulario_reserva.html`
**Problema:** Si el usuario no selecciona paquete y hace submit, `idPaquetesEventos` se envia como `NaN`.
**Accion:** Agregar validacion antes del fetch en el evento submit (linea 148):
```javascript
const selPaquete = document.getElementById('paquete');
if (!selPaquete.value) {
    alert('Selecciona un evento y un paquete primero');
    return;
}
```
(Ponerlo justo antes de `const opt = selPaquete.options[selPaquete.selectedIndex];`)

### Bug 3 — Prompt de IA pide datos en Cotizaciones y Disponibilidad
**Archivo:** `app/services/ia_service.py`
**Problema:** Las secciones 3 (COTIZACIONES) y 4 (DISPONIBILIDAD) del prompt aun dicen "Solicita la informacion necesaria" y "Comparte el formulario de reserva", causando que la IA pida datos que el formulario ya recolecta.
**Accion:** Cambiar lineas 157-161 y 165-168 para que digan "No solicites datos del evento, el formulario de reserva ya los solicita. Comparte inmediatamente el enlace del formulario."

**Seccion 3 (COTIZACIONES) — lineas 157-161 actuales:**
```
Si el cliente solicita precios o cotizaciones:
- No inventes montos.
- Explica que la cotizacion depende de la fecha, ubicacion, duracion, tipo de evento y cantidad de invitados.
- Solicita la informacion necesaria.
- Comparte el formulario de reserva.
```
**Cambiar a:**
```
Si el cliente solicita precios o cotizaciones:
- No inventes montos.
- No solicites datos del evento (fecha, tipo, invitados, ubicacion).
- El formulario de reserva ya los solicita.
- Comparte inmediatamente el enlace del formulario de reserva.
```

**Seccion 4 (DISPONIBILIDAD) — lineas 165-168 actuales:**
```
Si preguntan por disponibilidad:
- Indica que se debe validar la fecha.
- Solicita la fecha del evento si aun no la indico.
- Comparte el formulario de reserva.
```
**Cambiar a:**
```
Si preguntan por disponibilidad:
- Indica que se debe validar la fecha.
- No solicites datos del evento.
- El formulario de reserva ya los solicita.
- Comparte inmediatamente el enlace del formulario de reserva.
```

### Bug 4 — Bridge no responde si FastAPI esta caido
**Archivo:** `whatsapp-bridge/bridge.js`
**Problema:** Si FastAPI no responde, el error se captura pero el cliente nunca recibe respuesta.
**Accion:** Agregar mensaje de error al cliente en el catch (linea 44-46):
```javascript
} catch (err) {
    console.error('Error conectando con FastAPI:', err.message);
    await msg.reply('Lo siento, el servicio no esta disponible en este momento. Intentalo mas tarde.');
}
```

---

## 🟡 Mejoras (No criticas pero recomendadas)

### Mejora 1 — Sin feedback si telefono es invalido en formularios
**Archivo:** `app/api/routes/formularios.py`
**Problema:** Si alguien accede a `/formulario/reserva?telefono=INEXISTENTE`, el HTML se renderiza igual y el POST solo falla con JSON.
**Accion:** En el HTML, al carga inicial, hacer un fetch a `/api/clientes?telefono=XXX` para verificar si el cliente existe y mostrar mensaje si no.

### Mejora 2 — Variables obsoletas en config.py
**Archivo:** `app/core/config.py`
**Problema:** `form_cliente_url` y `form_reserva_url` (Google Forms) ya no se usan en el flujo actual.
**Accion:** Opcional: eliminar o comentar las lineas 16-17.

### Mejora 3 — Palabra "evento" causa falsos positivos en IA
**Archivo:** `app/services/ia_service.py` linea 144
**Problema:** "evento" esta en la lista de palabras que activan el flujo de reserva. Si alguien dice "que evento tienen?" la IA podria activar reserva cuando solo es consulta.
**Accion:** Evaluar si conviene mover "evento" a solo consultas generales.

---

## 📄 Documentacion desactualizada (Ya corregida)

| Archivo | Estado |
|---------|--------|
| `README.md` | ✅ Actualizado |
| `docs/ACTUALIZACION_BRIDGE_LOCAL.md` | ✅ Actualizado |
| `creacion_bd.sql` | ✅ Agregado `precio_unitario` |
| `docs/BD.md` | ✅ Creado (nuevo) |
