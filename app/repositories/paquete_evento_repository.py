from app.core.database import get_connection


class PaqueteEventoRepository:
    def get_activos_para_ia(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT nombre_paquete, descripcion, precio, estado
                    FROM paquetes
                    WHERE estado = 'activo'
                    ORDER BY idPaquetes
                    """
                )
                return cur.fetchall()

    def get_by_id(self, paquete_evento_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPaquetesEventos, idPaquetes, idEventos
                    FROM paquetes_eventos
                    WHERE idPaquetesEventos = %s
                    """,
                    (paquete_evento_id,),
                )
                return cur.fetchone()

    def get_by_evento(self, evento_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPaquetesEventos, idPaquetes, idEventos
                    FROM paquetes_eventos
                    WHERE idEventos = %s
                    """,
                    (evento_id,),
                )
                return cur.fetchall()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO paquetes_eventos (idPaquetes, idEventos)
                    VALUES (%s, %s)
                    """,
                    (data["idPaquetes"], data["idEventos"]),
                )

    def delete(self, paquete_evento_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM paquetes_eventos WHERE idPaquetesEventos = %s",
                    (paquete_evento_id,),
                )
                return cur.rowcount > 0