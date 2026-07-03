from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
from pydantic import BaseModel
from datetime import date
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.paquete_evento_repository import PaqueteEventoRepository
from app.repositories.paquete_repository import PaqueteRepository
from app.schemas.reserva import ReservaCreate
from app.core.database import get_connection
router = APIRouter(tags=["formularios"])
class FormularioReservaRequest(BaseModel):
    telefono: str
    fecha_evento: date
    hora_evento: str
    idPaquetesEventos: int
    cantidad: int = 1
@router.get("/formulario/cliente", response_class=HTMLResponse)
async def formulario_cliente(telefono: str):
    html_path = Path(__file__).parent.parent.parent / "templates" / "formulario_clientes.html"
    html = html_path.read_text(encoding="utf-8")
    return html
@router.get("/formulario/reserva", response_class=HTMLResponse)
async def formulario_reserva(telefono: str):
    html_path = Path(__file__).parent.parent.parent / "templates" / "formulario_reserva.html"
    html = html_path.read_text(encoding="utf-8")
    return html
@router.post("/formulario/reserva")
async def crear_reserva(data: FormularioReservaRequest):
    cliente_repo = ClienteRepository()
    pe_repo = PaqueteEventoRepository()
    paquete_repo = PaqueteRepository()
    cliente = cliente_repo.get_by_telefono(data.telefono)
    if not cliente:
        return JSONResponse(status_code=404, content={"error": "Cliente no encontrado"})
    id_clientes = cliente[0]
    pe = pe_repo.get_by_id(data.idPaquetesEventos)
    if not pe:
        return JSONResponse(status_code=404, content={"error": "Relacion paquete-evento no encontrada"})
    id_paquetes = pe[1]
    paquete = paquete_repo.get_by_id(id_paquetes)
    if not paquete:
        return JSONResponse(status_code=404, content={"error": "Paquete no encontrado"})
    precio = paquete[3]
    subtotal = round(float(precio) * data.cantidad, 2)
    total = subtotal
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO reservas (idClientes, fecha_evento, hora_evento, estado, total_reserva)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING idReservas
                """,
                (id_clientes, data.fecha_evento, data.hora_evento, "pendiente", total),
            )
            id_reserva = cur.fetchone()[0]
            cur.execute(
                """
                INSERT INTO detalle_reserva (idReservas, idPaquetesEventos, cantidad, precio_unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_reserva, data.idPaquetesEventos, data.cantidad, precio, subtotal),
            )
            adelanto = round(total / 2, 2)
            cur.execute(
                """
                INSERT INTO pagos (idReservas, monto_pagado, metodo_pago, estado, referencia)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (id_reserva, adelanto, "Pendiente", "pendiente", f"Adelanto 50% reserva #{id_reserva}"),
            )
            conn.commit()
    return {
        "mensaje": "Reserva registrada correctamente",
        "idReserva": id_reserva,
        "total": total,
        "adelanto": adelanto,
        "estado": "pendiente"
    }