from app.core.database import get_connection


class EventoRepository:
    def get_all_para_ia(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT nombre, descripcion
                    FROM eventos
                    ORDER BY idEventos
                    """
                )
                return cur.fetchall()