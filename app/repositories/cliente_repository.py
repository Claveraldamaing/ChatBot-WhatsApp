from app.core.database import get_connection

class ClienteRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idClientes, nombre, telefono, email, fecha_registro
                    FROM clientes
                    ORDER BY idClientes
                    """
                )
                return cur.fetchall()

    def get_by_id(self, cliente_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idClientes, nombre, telefono, email, fecha_registro
                    FROM clientes
                    WHERE idClientes = %s
                    """,
                    (cliente_id,),
                )
                return cur.fetchone()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO clientes (nombre, telefono, email)
                    VALUES (%s, %s, %s)
                    """,
                    (data["nombre"], data["telefono"], data["email"]),
                )

    def update(self, cliente_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE clientes
                    SET nombre = %s, telefono = %s, email = %s
                    WHERE idClientes = %s
                    """,
                    (data["nombre"], data["telefono"], data["email"], cliente_id),
                )
                return cur.rowcount > 0

    def delete(self, cliente_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM clientes WHERE idClientes = %s",
                    (cliente_id,),
                )
                return cur.rowcount > 0
