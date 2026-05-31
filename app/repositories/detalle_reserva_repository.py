from app.core.database import get_connection


class DetalleReservaRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idDetalleReserva, idReservas, idPaquetesEventos,
                           cantidad, subtotal,
                           (cantidad * subtotal) AS subtotal
                    FROM detalle_reserva
                    ORDER BY idDetalleReserva
                    """
                )
                return cur.fetchall()

    def get_by_id(self, detalle_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idDetalleReserva, idReservas, idPaquetesEventos,
                           cantidad, subtotal,
                           (cantidad * subtotal) AS subtotal
                    FROM detalle_reserva
                    WHERE idDetalleReserva = %s
                    """,
                    (detalle_id,),
                )
                return cur.fetchone()

    def get_by_reserva(self, reserva_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idDetalle_Reserva, idReservas, idPaquetes,
                           cantidad, precio_unitario,
                           (cantidad * precio_unitario) AS subtotal
                    FROM detalle_reserva
                    WHERE idReservas = %s
                    ORDER BY idDetalle_Reserva
                    """,
                    (reserva_id,),
                )
                return cur.fetchall()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO detalle_reserva (idReservas, idPaquetes, cantidad, precio_unitario)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        data["idReservas"],
                        data["idPaquetes"],
                        data["cantidad"],
                        data["precio_unitario"],
                    ),
                )

    def update(self, detalle_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE detalle_reserva
                    SET idReservas = %s, idPaquetes = %s,
                        cantidad = %s, precio_unitario = %s
                    WHERE idDetalle_Reserva = %s
                    """,
                    (
                        data["idReservas"],
                        data["idPaquetes"],
                        data["cantidad"],
                        data["precio_unitario"],
                        detalle_id,
                    ),
                )
                return cur.rowcount > 0

    def delete(self, detalle_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM detalle_reserva WHERE idDetalle_Reserva = %s",
                    (detalle_id,),
                )
                return cur.rowcount > 0