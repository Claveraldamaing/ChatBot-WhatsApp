from app.core.database import get_connection
class UsuarioRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idUsuario, nombre, email, password_hash, rol, estado, fecha_registro
                    FROM usuarios
                    ORDER BY idUsuario
                    """
                )
                return cur.fetchall()
    def get_by_id(self, usuario_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idUsuario, nombre, email, password_hash, rol, estado, fecha_registro
                    FROM usuarios
                    WHERE idUsuario = %s
                    """,
                    (usuario_id,),
                )
                return cur.fetchone()
    def get_by_email(self, email: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idUsuario, nombre, email, password_hash, rol, estado, fecha_registro
                    FROM usuarios
                    WHERE email = %s
                    """,
                    (email,),
                )
                return cur.fetchone()
    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO usuarios (nombre, email, password_hash, rol, estado)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING idUsuario
                    """,
                    (data["nombre"], data["email"], data["password_hash"], data["rol"], data["estado"]),
                )
                return cur.fetchone()[0]
    def update(self, usuario_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE usuarios
                    SET nombre = %s, email = %s, password_hash = %s, rol = %s, estado = %s
                    WHERE idUsuario = %s
                    """,
                    (data["nombre"], data["email"], data["password_hash"], data["rol"], data["estado"], usuario_id),
                )
                return cur.rowcount > 0
    def delete(self, usuario_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM usuarios WHERE idUsuario = %s",
                    (usuario_id,),
                )
                return cur.rowcount > 0