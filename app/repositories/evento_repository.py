from app.core.database import get_connection


class EventoRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idEventos, nombre, descripcion
                    FROM eventos
                    ORDER BY idEventos
                    """
                )
                return cur.fetchall()

    def get_by_id(self, evento_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idEventos, nombre, descripcion
                    FROM eventos
                    WHERE idEventos = %s
                    """,
                    (evento_id,),
                )
                return cur.fetchone()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO eventos (nombre, descripcion)
                    VALUES (%s, %s)
                    """,
                    (data["nombre"], data["descripcion"]),
                )

    def update(self, evento_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE eventos
                    SET nombre = %s, descripcion = %s
                    WHERE idEventos = %s
                    """,
                    (data["nombre"], data["descripcion"], evento_id),
                )
                return cur.rowcount > 0

    def delete(self, evento_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM eventos WHERE idEventos = %s",
                    (evento_id,),
                )
                return cur.rowcount > 0