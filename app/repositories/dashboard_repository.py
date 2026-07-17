from app.core.database import get_connection


class DashboardRepository:
    def get_stats(self) -> dict:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT COUNT(*) FROM eventos
                """)
                total_eventos = cur.fetchone()[0]

                cur.execute("""
                    SELECT
                        COUNT(*) FILTER (WHERE estado = 'pendiente') AS pendientes,
                        COUNT(*) FILTER (WHERE estado = 'confirmada') AS confirmadas,
                        COUNT(*) FILTER (WHERE estado = 'completada') AS completadas,
                        COUNT(*) FILTER (WHERE estado = 'cancelada') AS canceladas,
                        COUNT(*) AS total
                    FROM reservas
                """)
                r = cur.fetchone()
                reservas = {
                    "pendientes": r[0],
                    "confirmadas": r[1],
                    "completadas": r[2],
                    "canceladas": r[3],
                    "total": r[4],
                }

                cur.execute("""
                    SELECT COALESCE(SUM(monto_pagado), 0)
                    FROM pagos WHERE estado = 'pagado'
                """)
                ingresos_cobrados = cur.fetchone()[0]

                cur.execute("""
                    SELECT COALESCE(SUM(total_reserva), 0)
                    FROM reservas
                    WHERE estado IN ('pendiente', 'confirmada')
                """)
                pendiente_cobro = cur.fetchone()[0]

                cur.execute("SELECT COUNT(*) FROM clientes")
                total_clientes = cur.fetchone()[0]

                cur.execute("""
                    SELECT COUNT(*) FROM recordatorios WHERE estado = 'pendiente'
                """)
                recordatorios_pendientes = cur.fetchone()[0]

                cur.execute("""
                    SELECT r.idReservas, r.fecha_evento, r.hora_evento,
                           r.estado, r.total_reserva,
                           c.nombre AS cliente_nombre
                    FROM reservas r
                    JOIN clientes c ON c.idClientes = r.idClientes
                    WHERE r.estado IN ('pendiente', 'confirmada')
                      AND r.fecha_evento >= CURRENT_DATE
                    ORDER BY r.fecha_evento ASC
                    LIMIT 1
                """)
                prox = cur.fetchone()
                proximo_evento = None
                if prox:
                    proximo_evento = {
                        "id": prox[0],
                        "fecha_evento": str(prox[1]),
                        "hora_evento": str(prox[2]),
                        "estado": prox[3],
                        "total_reserva": prox[4],
                        "cliente_nombre": prox[5],
                    }

                cur.execute("""
                    SELECT
                        TO_CHAR(p.fecha_pago, 'YYYY-MM') AS mes,
                        SUM(p.monto_pagado) AS total
                    FROM pagos p
                    WHERE p.estado = 'pagado'
                    GROUP BY mes
                    ORDER BY mes DESC
                    LIMIT 6
                """)
                ingresos_por_mes = [
                    {"mes": row[0], "total": float(row[1])}
                    for row in cur.fetchall()
                ]
                ingresos_por_mes.reverse()

                cur.execute("""
                    SELECT r.idReservas, r.fecha_evento, r.hora_evento,
                           r.estado, r.total_reserva,
                           c.nombre AS cliente_nombre
                    FROM reservas r
                    JOIN clientes c ON c.idClientes = r.idClientes
                    ORDER BY r.idReservas DESC
                    LIMIT 5
                """)
                ultimas_reservas = [
                    {
                        "id": row[0],
                        "fecha_evento": str(row[1]),
                        "hora_evento": str(row[2]),
                        "estado": row[3],
                        "total_reserva": row[4],
                        "cliente_nombre": row[5],
                    }
                    for row in cur.fetchall()
                ]

                cur.execute("""
                    SELECT idRecordatorio, idReservas, tipo, mensaje,
                           fecha_programada, estado
                    FROM recordatorios
                    WHERE estado = 'pendiente'
                    ORDER BY fecha_programada ASC
                    LIMIT 4
                """)
                recordatorios = [
                    {
                        "id": row[0],
                        "idReservas": row[1],
                        "tipo": row[2],
                        "mensaje": row[3],
                        "fecha_programada": str(row[4]),
                        "estado": row[5],
                    }
                    for row in cur.fetchall()
                ]

                return {
                    "total_eventos": total_eventos,
                    "reservas": reservas,
                    "ingresos_cobrados": float(ingresos_cobrados),
                    "pendiente_cobro": float(pendiente_cobro),
                    "total_clientes": total_clientes,
                    "recordatorios_pendientes": recordatorios_pendientes,
                    "proximo_evento": proximo_evento,
                    "ingresos_por_mes": ingresos_por_mes,
                    "ultimas_reservas": ultimas_reservas,
                    "recordatorios": recordatorios,
                }
