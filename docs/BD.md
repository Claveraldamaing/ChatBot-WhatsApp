# Base de Datos — ChatBot WhatsApp

PostgreSQL con 12 tablas. Datos de prueba en `inserts.sql`.

---

## Diagrama de relaciones

```
clientes ──── mensajes_ia
    │
    └──── reservas ──── detalle_reserva ──── paquetes_eventos ──── eventos
              │                                           └──── paquetes
              ├──── pagos
              ├──── formularios ──── tipo_formulario
              └──── recordatorios

usuarios (independiente)
```

---

## 1. `clientes`

Registro de clientes que escriben por WhatsApp.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idClientes | `SERIAL` | `PRIMARY KEY` | ID unico del cliente |
| nombre | `VARCHAR(100)` | `NOT NULL` | Nombre completo |
| telefono | `VARCHAR(20)` | `NOT NULL, UNIQUE` | Numero de WhatsApp |
| email | `VARCHAR(100)` | — | Correo electronico (opcional) |
| fecha_registro | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Fecha de registro |

```sql
INSERT INTO clientes (nombre, telefono, email) VALUES
('Juan Perez', '987654321', 'juan@gmail.com'),
('Maria Lopez', '912345678', 'maria@gmail.com');
```

---

## 2. `mensajes_ia`

Historial de conversaciones entre el cliente y la IA.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idMensajes_ia | `SERIAL` | `PRIMARY KEY` | ID unico del mensaje |
| idClientes | `INT` | `NOT NULL, FK → clientes(idClientes)` | Cliente que envia/recibe |
| rol | `VARCHAR(20)` | `NOT NULL` | `'cliente'` o `'asistente'` |
| contenido | `TEXT` | `NOT NULL` | Texto del mensaje |
| tipo | `VARCHAR(30)` | — | `'entrada'`, `'respuesta'`, `'texto'` |
| fecha_hora_mensaje | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Momento del mensaje |
| estado | `VARCHAR(30)` | — | `'activo'`, `'recibido'`, `'enviado'` |
| tiene_reserva | `BOOLEAN` | `DEFAULT FALSE` | Indica si genero una reserva |

```sql
INSERT INTO mensajes_ia (idClientes, rol, contenido, tipo, estado, tiene_reserva) VALUES
(1, 'cliente', 'Hola, quiero informacion del paquete premium', 'texto', 'recibido', false),
(1, 'bot', 'Claro, el paquete premium incluye decoracion y animacion', 'texto', 'enviado', false);
```

---

## 3. `eventos`

Tipos de evento que ofrece la empresa.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idEventos | `SERIAL` | `PRIMARY KEY` | ID unico del evento |
| nombre | `VARCHAR(100)` | `NOT NULL` | Nombre del evento |
| descripcion | `TEXT` | — | Descripcion detallada |

```sql
INSERT INTO eventos (nombre, descripcion) VALUES
('Cumpleaños Infantil', 'Evento para fiestas infantiles'),
('Baby Shower', 'Evento para celebraciones baby shower');
```

---

## 4. `paquetes`

Paquetes de servicios que se pueden contratar.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idPaquetes | `SERIAL` | `PRIMARY KEY` | ID unico del paquete |
| nombre_paquete | `VARCHAR(100)` | `NOT NULL` | Nombre del paquete |
| descripcion | `TEXT` | — | Descripcion del servicio |
| precio | `NUMERIC(10,2)` | `NOT NULL` | Precio en soles |
| estado | `VARCHAR(30)` | `DEFAULT 'activo'` | `'activo'` o `'inactivo'` |

```sql
INSERT INTO paquetes (nombre_paquete, descripcion, precio, estado) VALUES
('Basico', 'Incluye animacion simple', 300.00, 'activo'),
('Premium', 'Incluye animacion + decoracion', 500.00, 'activo'),
('Hora Extra', 'Hora adicional del servicio', 80.00, 'activo');
```

---

## 5. `paquetes_eventos`

Relacion muchos-a-muchos entre eventos y paquetes.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idPaquetesEventos | `SERIAL` | `PRIMARY KEY` | ID unico de la relacion |
| idEventos | `INT` | `NOT NULL, FK → eventos(idEventos)` | Evento asociado |
| idPaquetes | `INT` | `NOT NULL, FK → paquetes(idPaquetes)` | Paquete asociado |

```sql
INSERT INTO paquetes_eventos (idEventos, idPaquetes) VALUES
(1, 1),  -- Cumpleaños → Basico
(1, 2),  -- Cumpleaños → Premium
(1, 3),  -- Cumpleaños → Hora Extra
(2, 2);  -- Baby Shower → Premium
```

---

## 6. `reservas`

Reservas realizadas por los clientes.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idReservas | `SERIAL` | `PRIMARY KEY` | ID unico de la reserva |
| idClientes | `INT` | `NOT NULL, FK → clientes(idClientes)` | Cliente que reserva |
| fecha_reserva | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Momento de la reserva |
| fecha_evento | `DATE` | `NOT NULL` | Fecha del evento |
| hora_evento | `TIME` | `NOT NULL` | Hora del evento |
| estado | `VARCHAR(30)` | `DEFAULT 'pendiente'` | `'pendiente'`, `'confirmada'`, `'cancelada'` |
| total_reserva | `NUMERIC(10,2)` | `DEFAULT 0` | Total a pagar |

```sql
INSERT INTO reservas (idClientes, fecha_evento, hora_evento, estado, total_reserva) VALUES
(1, '2026-06-20', '17:00:00', 'pendiente', 580.00);
```

---

## 7. `detalle_reserva`

Items dentro de cada reserva (que paquete, cantidad, precio).

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idDetalleReserva | `SERIAL` | `PRIMARY KEY` | ID unico del detalle |
| idReservas | `INT` | `NOT NULL, FK → reservas(idReservas)` | Reserva a la que pertenece |
| idPaquetesEventos | `INT` | `NOT NULL, FK → paquetes_eventos(idPaquetesEventos)` | Paquete-evento contratado |
| cantidad | `INT` | `DEFAULT 1` | Cantidad de unidades |
| precio_unitario | `NUMERIC(10,2)` | `NOT NULL` | Precio por unidad |
| subtotal | `NUMERIC(10,2)` | `NOT NULL` | `precio_unitario * cantidad` |

```sql
INSERT INTO detalle_reserva (cantidad, precio_unitario, subtotal, idPaquetesEventos, idReservas) VALUES
(1, 500.00, 500.00, 2, 1),
(1, 80.00, 80.00, 3, 1);
```

---

## 8. `pagos`

Pagos realizados para las reservas.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idPagos | `SERIAL` | `PRIMARY KEY` | ID unico del pago |
| idReservas | `INT` | `NOT NULL, FK → reservas(idReservas)` | Reserva asociada |
| monto_pagado | `NUMERIC(10,2)` | `NOT NULL` | Monto pagado |
| metodo_pago | `VARCHAR(50)` | `NOT NULL` | `'Yape'`, `'Transferencia'`, `'Efectivo'` |
| estado | `VARCHAR(30)` | `DEFAULT 'pendiente'` | `'pendiente'`, `'pagado'`, `'rechazado'` |
| fecha_pago | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Fecha del pago |
| referencia | `VARCHAR(100)` | — | Numero de referencia o comprobante |

```sql
INSERT INTO pagos (idReservas, monto_pagado, metodo_pago, estado, referencia) VALUES
(1, 200.00, 'Yape', 'pagado', 'YAPE-982341');
```

---

## 9. `tipo_formulario`

Catalogos de tipos de formulario disponibles.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idTipoFormulario | `SERIAL` | `PRIMARY KEY` | ID unico del tipo |
| nombre_tipo | `VARCHAR(50)` | `NOT NULL` | Nombre (ej: `'reserva'`, `'satisfaccion'`) |
| descripcion | `TEXT` | — | Descripcion del formulario |
| link_formulario | `TEXT` | `NOT NULL` | URL del formulario |
| estado | `VARCHAR(30)` | `DEFAULT 'activo'` | `'activo'` o `'inactivo'` |

```sql
INSERT INTO tipo_formulario (nombre_tipo, descripcion, link_formulario, estado) VALUES
('reserva', 'Formulario de reserva', 'https://forms.google.com/reserva', 'activo'),
('satisfaccion', 'Formulario de satisfaccion', 'https://forms.google.com/satisfaccion', 'activo');
```

---

## 10. `formularios`

Formularios enviados a clientes y sus respuestas.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idFormulario | `SERIAL` | `PRIMARY KEY` | ID unico del formulario |
| idTipoFormulario | `INT` | `NOT NULL, FK → tipo_formulario(idTipoFormulario)` | Tipo de formulario |
| idReservas | `INT` | `NOT NULL, FK → reservas(idReservas)` | Reserva asociada |
| fecha_envio | `TIMESTAMP` | — | Cuando se envio al cliente |
| fecha_respuesta | `TIMESTAMP` | — | Cuando el cliente respondio |
| estado | `VARCHAR(30)` | `DEFAULT 'pendiente'` | `'pendiente'`, `'respondido'` |
| respuesta_json | `JSONB` | — | Datos de la respuesta en JSON |
| notificado_dueno | `BOOLEAN` | `DEFAULT FALSE` | Si se notifico al admin |
| fecha_notificacion | `TIMESTAMP` | — | Cuando se notifico al admin |

```sql
INSERT INTO formularios (idTipoFormulario, idReservas, fecha_envio, estado, respuesta_json, notificado_dueno) VALUES
(1, 1, CURRENT_TIMESTAMP, 'respondido', '{"tematica":"Spiderman","direccion":"Av Peru 123"}', true);
```

---

## 11. `recordatorios`

Recordatorios programados para eventos.

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idRecordatorio | `SERIAL` | `PRIMARY KEY` | ID unico del recordatorio |
| idReservas | `INT` | `NOT NULL, FK → reservas(idReservas)` | Reserva asociada |
| tipo | `VARCHAR(50)` | `NOT NULL` | `'antes_evento'`, `'pago_pendiente'`, `'post_evento'` |
| mensaje | `TEXT` | `NOT NULL` | Contenido del recordatorio |
| fecha_programada | `TIMESTAMP` | `NOT NULL` | Cuando enviar el recordatorio |
| fecha_envio | `TIMESTAMP` | — | Cuando se envio realmente |
| estado | `VARCHAR(30)` | `DEFAULT 'pendiente'` | `'pendiente'`, `'enviado'`, `'cancelado'` |

```sql
INSERT INTO recordatorios (idReservas, tipo, mensaje, fecha_programada, estado) VALUES
(1, 'antes_evento', 'Tu evento sera mañana 🎉', '2026-06-19 10:00:00', 'pendiente');
```

---

## 12. `usuarios`

Usuarios del sistema (panel de administracion).

| Columna | Tipo | Restricciones | Descripcion |
|---------|------|---------------|-------------|
| idUsuario | `SERIAL` | `PRIMARY KEY` | ID unico del usuario |
| nombre | `VARCHAR(100)` | `NOT NULL` | Nombre del usuario |
| email | `VARCHAR(100)` | `NOT NULL, UNIQUE` | Email de inicio de sesion |
| password_hash | `TEXT` | `NOT NULL` | Hash de la contrasena |
| rol | `VARCHAR(30)` | `NOT NULL` | `'admin'`, `'supervisor'` |
| estado | `VARCHAR(30)` | `DEFAULT 'activo'` | `'activo'`, `'inactivo'` |
| fecha_registro | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Fecha de creacion |

```sql
INSERT INTO usuarios (nombre, email, password_hash, rol, estado) VALUES
('Administrador', 'admin@gmail.com', 'hash123', 'admin', 'activo');
```

---

## Resumen de Foreign Keys

| Tabla | FK | Referencia |
|-------|----|------------|
| mensajes_ia | idClientes | clientes(idClientes) |
| reservas | idClientes | clientes(idClientes) |
| detalle_reserva | idReservas | reservas(idReservas) |
| detalle_reserva | idPaquetesEventos | paquetes_eventos(idPaquetesEventos) |
| paquetes_eventos | idEventos | eventos(idEventos) |
| paquetes_eventos | idPaquetes | paquetes(idPaquetes) |
| pagos | idReservas | reservas(idReservas) |
| formularios | idTipoFormulario | tipo_formulario(idTipoFormulario) |
| formularios | idReservas | reservas(idReservas) |
| recordatorios | idReservas | reservas(idReservas) |
