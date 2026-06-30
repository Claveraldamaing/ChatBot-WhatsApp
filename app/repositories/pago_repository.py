from app.core.database import get_connection


class PagoRepository:
    def get_all(self):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPagos, idReservas, monto_pagado, metodo_pago,
                           estado, fecha_pago, referencia
                    FROM pagos
                    ORDER BY idPagos
                    """
                )
                return cur.fetchall()

    def get_by_id(self, pago_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPagos, idReservas, monto_pagado, metodo_pago,
                           estado, fecha_pago, referencia
                    FROM pagos
                    WHERE idPagos = %s
                    """,
                    (pago_id,),
                )
                return cur.fetchone()

    def get_by_reserva(self, reserva_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT idPagos, idReservas, monto_pagado, metodo_pago,
                           estado, fecha_pago, referencia
                    FROM pagos
                    WHERE idReservas = %s
                    ORDER BY idPagos
                    """,
                    (reserva_id,),
                )
                return cur.fetchall()

    def create(self, data: dict):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO pagos (idReservas, monto_pagado, metodo_pago, estado, referencia)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        data["idReservas"],
                        data["monto_pagado"],
                        data["metodo_pago"],
                        data["estado"],
                        data["referencia"],
                    ),
                )

    def update(self, pago_id: int, data: dict) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE pagos
                    SET idReservas = %s, monto_pagado = %s, metodo_pago = %s,
                        estado = %s, referencia = %s
                    WHERE idPagos = %s
                    """,
                    (
                        data["idReservas"],
                        data["monto_pagado"],
                        data["metodo_pago"],
                        data["estado"],
                        data["referencia"],
                        pago_id,
                    ),
                )
                return cur.rowcount > 0

    def delete(self, pago_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM pagos WHERE idPagos = %s",
                    (pago_id,),
                )
                return cur.rowcount > 0
            
    def update_estado(self, pago_id: int, estado: str) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE pagos SET estado = %s WHERE idPagos = %s",
                    (estado, pago_id),
                )
                return cur.rowcount > 0    
    def get_by_cliente(self, cliente_id: int):
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT p.idPagos, p.idReservas, p.monto_pagado, p.metodo_pago,
                        p.estado, p.fecha_pago, p.referencia,
                        r.total_reserva, r.estado AS estado_reserva
                    FROM pagos p
                    JOIN reservas r ON r.idReservas = p.idReservas
                    WHERE r.idClientes = %s
                    ORDER BY p.fecha_pago DESC
                """, (cliente_id,))
                return cur.fetchall()
            
            