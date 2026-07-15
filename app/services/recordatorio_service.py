from datetime import timedelta
from app.repositories.recordatorio_repository import RecordatorioRepository
from app.repositories.reserva_repository import ReservaRepository
from app.schemas.recordatorio import RecordatorioCreate, RecordatorioResponse
class RecordatorioService:
    def __init__(self):
        self.repository = RecordatorioRepository()
    def list_recordatorios(self) -> list[RecordatorioResponse]:
        items = self.repository.get_all()
        return [RecordatorioResponse(**self._normalize(r)) for r in items]
    def get_recordatorio(self, recordatorio_id: int) -> RecordatorioResponse | None:
        item = self.repository.get_by_id(recordatorio_id)
        if item is None:
            return None
        return RecordatorioResponse(**self._normalize(item))
    def list_by_reserva(self, reserva_id: int) -> list[RecordatorioResponse]:
        items = self.repository.get_by_reserva(reserva_id)
        return [RecordatorioResponse(**self._normalize(r)) for r in items]
    def create_recordatorio(self, data: RecordatorioCreate):
        self.repository.create(data.model_dump())
    def update_recordatorio(self, recordatorio_id: int, data: RecordatorioCreate) -> bool:
        return self.repository.update(recordatorio_id, data.model_dump())
    def delete_recordatorio(self, recordatorio_id: int) -> bool:
        return self.repository.delete(recordatorio_id)
    def marcar_enviado(self, recordatorio_id: int) -> bool:
        return self.repository.update_estado(recordatorio_id, "enviado")
    def generar_para_reserva(self, reserva_id: int) -> bool:
        reserva_repo = ReservaRepository()
        reserva = reserva_repo.get_by_id(reserva_id)
        if not reserva:
            return False
        # reserva: (idReservas, idClientes, fecha_reserva, fecha_evento, hora_evento, estado, total_reserva)
        fecha_evento = reserva[3]
        hora_evento = str(reserva[4])
        total = reserva[6]
        reserva_estado = reserva[5]
        recordatorios = []
        recordatorios.append({
            "idReservas": reserva_id,
            "tipo": "antes_evento",
            "mensaje": f"Recordatorio: tu evento es mañana {fecha_evento} a las {hora_evento}. Todo listo!",
            "fecha_programada": fecha_evento - timedelta(days=1),
            "estado": "pendiente",
        })
        if reserva_estado == "pendiente":
            recordatorios.append({
                "idReservas": reserva_id,
                "tipo": "pago_pendiente",
                "mensaje": f"Aun tienes un pago pendiente de S/ {total}. Realizalo para confirmar tu reserva.",
                "fecha_programada": fecha_evento - timedelta(days=3),
                "estado": "pendiente",
            })
        recordatorios.append({
            "idReservas": reserva_id,
            "tipo": "post_evento",
            "mensaje": "Gracias por tu preferencia! Cuentanos como fue tu experiencia.",
            "fecha_programada": fecha_evento + timedelta(days=1),
            "estado": "pendiente",
        })
        for r in recordatorios:
            self.repository.create(r)
        return True
    def _normalize(self, r: tuple) -> dict:
        return {
            "id": r[0],
            "idReservas": r[1],
            "tipo": r[2],
            "mensaje": r[3],
            "fecha_programada": r[4],
            "fecha_envio": r[5],
            "estado": r[6],
        }