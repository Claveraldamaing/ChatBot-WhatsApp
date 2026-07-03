from app.core.database import get_connection
from app.repositories.mensajes_ia_repository import MensajesIARepository
from app.schemas.mensaje_ia import MensajeIAResponse
class MensajesIAService:
    def __init__(self):
        self.repository = MensajesIARepository()
    def list_by_cliente(self, cliente_id: int, limit: int = 50) -> list[MensajeIAResponse]:
        mensajes = self.repository.get_by_cliente(cliente_id, limit=limit)
        mensajes = list(reversed(mensajes))
        return [MensajeIAResponse(**self._normalize(m)) for m in mensajes]
    def delete(self, mensaje_id: int) -> bool:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM mensajes_ia WHERE idMensajes_ia = %s",
                    (mensaje_id,),
                )
                return cur.rowcount > 0
    def _normalize(self, m: tuple) -> dict:
        return {
            "id": m[0],
            "idClientes": m[1],
            "rol": m[2],
            "contenido": m[3],
            "tipo": m[4],
            "fecha_hora_mensaje": m[5],
            "estado": m[6],
            "tiene_reserva": m[7],
        }