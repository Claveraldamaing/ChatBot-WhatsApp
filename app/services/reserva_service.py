from app.repositories.reserva_repository import ReservaRepository
from app.schemas.reserva import ReservaCreate, ReservaResponse
class ReservaService:
    def __init__(self):
        self.repository = ReservaRepository()
    def list_reservas(self) -> list[ReservaResponse]:
        reservas = self.repository.get_all()
        return [ReservaResponse(**self._normalize(r)) for r in reservas]
    def get_reserva(self, reserva_id: int) -> ReservaResponse | None:
        reserva = self.repository.get_by_id(reserva_id)
        if reserva is None:
            return None
        return ReservaResponse(**self._normalize(reserva))
    def list_by_cliente(self, cliente_id: int) -> list[ReservaResponse]:
        reservas = self.repository.get_by_cliente(cliente_id)
        return [ReservaResponse(**self._normalize(r)) for r in reservas]
    def create_reserva(self, data: ReservaCreate) -> int:
        reserva_id = self.repository.create(data.model_dump())
        from app.services.recordatorio_service import RecordatorioService
        RecordatorioService().generar_para_reserva(reserva_id)
        return reserva_id
    def update_reserva(self, reserva_id: int, data: ReservaCreate) -> bool:
        return self.repository.update(reserva_id, data.model_dump())
    def delete_reserva(self, reserva_id: int) -> bool:
        return self.repository.delete(reserva_id)
    def _normalize(self, reserva: tuple) -> dict:
        return {
            "id": reserva[0],
            "idClientes": reserva[1],
            "fecha_reserva": reserva[2],
            "fecha_evento": reserva[3],
            "hora_evento": str(reserva[4]),
            "estado": reserva[5],
            "total_reserva": reserva[6],
        }
    def finalizar_pago(self, reserva_id: int) -> bool:
        from app.repositories.pago_repository import PagoRepository
        reserva = self.repository.get_by_id(reserva_id)
        if not reserva:
            return False
        if reserva[5] == "completada":
            return True
        if reserva[5] != "confirmada":
            return False
        pago_repo = PagoRepository()
        pagos_existentes = pago_repo.get_by_reserva(reserva_id)
        tiene_adelanto = any(p[4] == "pagado" for p in pagos_existentes)
        if not tiene_adelanto:
            return False
        monto_restante = reserva[6] / 2
        pago_repo.create({
            "idReservas": reserva_id,
            "monto_pagado": monto_restante,
            "metodo_pago": "Efectivo",
            "estado": "pagado",
            "referencia": f"Pago final reserva #{reserva_id}"
        })
        self.repository.update_estado(reserva_id, "completada")
        return True