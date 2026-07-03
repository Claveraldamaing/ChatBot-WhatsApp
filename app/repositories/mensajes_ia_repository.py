from app.core.database import get_connection


class MensajesIARepository:
    def get_by_cliente(self, id_clientes: int, limit: int = 8):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idMensajes_ia, idClientes, rol, contenido, tipo, fecha_hora_mensaje, estado, tiene_reserva
                    FROM mensajes_ia
                    WHERE idClientes = %s
                    ORDER BY fecha_hora_mensaje DESC
                    LIMIT %s
                    """,
                    (id_clientes, limit),
                )
                return cur.fetchall()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO mensajes_ia (
                        idClientes,
                        rol,
                        contenido,
                        tipo,
                        estado,
                        tiene_reserva
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        data["idClientes"],
                        data["rol"],
                        data["contenido"],
                        data.get("tipo"),
                        data.get("estado", "activo"),
                        data.get("tiene_reserva", False),
                    ),
                )

    def get_by_id(self, mensaje_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idMensajes_ia, idClientes, rol, contenido, tipo,
                        fecha_hora_mensaje, estado, tiene_reserva
                    FROM mensajes_ia
                    WHERE idMensajes_ia = %s
                    """,
                    (mensaje_id,),
                )
                return cur.fetchone()
    def delete(self, mensaje_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM mensajes_ia WHERE idMensajes_ia = %s",
                    (mensaje_id,),
                )
                return cur.rowcount > 0