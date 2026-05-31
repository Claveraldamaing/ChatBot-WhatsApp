from app.core.database import get_connection
 
 
class PaqueteRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPaquetes, nombre_paquete, descripcion, precio,estado
                    FROM paquetes
                    ORDER BY idPaquetes
                    """
                )
                return cur.fetchall()
 
    def get_by_id(self, paquete_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPaquetes, nombre_paquete, descripcion, precio,estado
                    FROM paquetes
                    WHERE idPaquetes = %s
                    """,
                    (paquete_id,),
                )
                return cur.fetchone()
 
    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO paquetes (nombre_paquete, descripcion, precio)
                    VALUES (%s, %s, %s)
                    """,
                    (data["nombre"], data["descripcion"], data["precio"]),
                )
 
    def update(self, paquete_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE paquetes
                    SET nombre_paquete = %s, descripcion = %s, precio = %s
                    WHERE idPaquetes = %s
                    """,
                    (data["nombre"], data["descripcion"], data["precio"], paquete_id),
                )
                return cur.rowcount > 0
 
    def delete(self, paquete_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM paquetes WHERE idPaquetes = %s",
                    (paquete_id,),
                )
                return cur.rowcount > 0
 