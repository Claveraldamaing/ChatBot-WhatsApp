from app.core.database import get_connection


class LidMapRepository:
    def get_by_lid(self, lid: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT telefono FROM lid_map WHERE lid = %s",
                    (lid,),
                )
                row = cur.fetchone()
                return row[0] if row else None

    def create(self, lid: str, telefono: str):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO lid_map (lid, telefono)
                    VALUES (%s, %s)
                    ON CONFLICT (lid) DO UPDATE SET telefono = EXCLUDED.telefono
                    """,
                    (lid, telefono),
                )
