from app.core.database import get_connection
class RecordatorioRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idRecordatorio, idReservas, tipo, mensaje,
                           fecha_programada, fecha_envio, estado
                    FROM recordatorios
                    ORDER BY idRecordatorio
                    """
                )
                return cur.fetchall()
    def get_by_id(self, recordatorio_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idRecordatorio, idReservas, tipo, mensaje,
                           fecha_programada, fecha_envio, estado
                    FROM recordatorios
                    WHERE idRecordatorio = %s
                    """,
                    (recordatorio_id,),
                )
                return cur.fetchone()
    def get_by_reserva(self, reserva_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idRecordatorio, idReservas, tipo, mensaje,
                           fecha_programada, fecha_envio, estado
                    FROM recordatorios
                    WHERE idReservas = %s
                    ORDER BY fecha_programada
                    """,
                    (reserva_id,),
                )
                return cur.fetchall()
    def get_pendientes(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idRecordatorio, idReservas, tipo, mensaje,
                           fecha_programada, fecha_envio, estado
                    FROM recordatorios
                    WHERE estado = 'pendiente'
                    ORDER BY fecha_programada
                    """
                )
                return cur.fetchall()
    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO recordatorios (idReservas, tipo, mensaje, fecha_programada, estado)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        data["idReservas"],
                        data["tipo"],
                        data["mensaje"],
                        data["fecha_programada"],
                        data["estado"],
                    ),
                )
    def update(self, recordatorio_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE recordatorios
                    SET idReservas = %s, tipo = %s, mensaje = %s,
                        fecha_programada = %s, estado = %s
                    WHERE idRecordatorio = %s
                    """,
                    (
                        data["idReservas"],
                        data["tipo"],
                        data["mensaje"],
                        data["fecha_programada"],
                        data["estado"],
                        recordatorio_id,
                    ),
                )
                return cur.rowcount > 0
    def delete(self, recordatorio_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM recordatorios WHERE idRecordatorio = %s",
                    (recordatorio_id,),
                )
                return cur.rowcount > 0
    def update_estado(self, recordatorio_id: int, estado: str) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE recordatorios
                    SET estado = %s, fecha_envio = NOW()
                    WHERE idRecordatorio = %s
                    """,
                    (estado, recordatorio_id),
                )
                return cur.rowcount > 0