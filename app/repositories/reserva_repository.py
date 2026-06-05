from app.core.database import get_connection


class ReservaRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idReservas, idClientes, fecha_reserva,
                           fecha_evento, hora_evento, estado, total_reserva
                    FROM reservas
                    ORDER BY idReservas
                    """
                )
                return cur.fetchall()

    def get_by_id(self, reserva_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idReservas, idClientes, fecha_reserva,
                           fecha_evento, hora_evento, estado, total_reserva
                    FROM reservas
                    WHERE idReservas = %s
                    """,
                    (reserva_id,),
                )
                return cur.fetchone()

    def get_by_cliente(self, cliente_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idReservas, idClientes, fecha_reserva,
                           fecha_evento, hora_evento, estado, total_reserva
                    FROM reservas
                    WHERE idClientes = %s
                    ORDER BY idReservas
                    """,
                    (cliente_id,),
                )
                return cur.fetchall()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO reservas (idClientes, fecha_evento, hora_evento, estado, total_reserva)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        data["idClientes"],
                        data["fecha_evento"],
                        data["hora_evento"],
                        data["estado"],
                        data["total_reserva"],
                    ),
                )

    def update(self, reserva_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE reservas
                    SET idClientes = %s, fecha_evento = %s, hora_evento = %s,
                        estado = %s, total_reserva = %s
                    WHERE idReservas = %s
                    """,
                    (
                        data["idClientes"],
                        data["fecha_evento"],
                        data["hora_evento"],
                        data["estado"],
                        data["total_reserva"],
                        reserva_id,
                    ),
                )
                return cur.rowcount > 0

    def delete(self, reserva_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM reservas WHERE idReservas = %s",
                    (reserva_id,),
                )
                return cur.rowcount > 0