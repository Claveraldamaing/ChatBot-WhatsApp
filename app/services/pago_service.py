from app.repositories.pago_repository import PagoRepository
from app.schemas.pago import PagoCreate, PagoResponse
class PagoService:
    def __init__(self):
        self.repository = PagoRepository()
    def list_pagos(self) -> list[PagoResponse]:
        pagos = self.repository.get_all()
        return [PagoResponse(**self._normalize(p)) for p in pagos]
    def get_pago(self, pago_id: int) -> PagoResponse | None:
        pago = self.repository.get_by_id(pago_id)
        if pago is None:
            return None
        return PagoResponse(**self._normalize(pago))
    def list_by_reserva(self, reserva_id: int) -> list[PagoResponse]:
        pagos = self.repository.get_by_reserva(reserva_id)
        return [PagoResponse(**self._normalize(p)) for p in pagos]
    def create_pago(self, data: PagoCreate):
        self.repository.create(data.model_dump())
    def update_pago(self, pago_id: int, data: PagoCreate) -> bool:
        return self.repository.update(pago_id, data.model_dump())
    def delete_pago(self, pago_id: int) -> bool:
        return self.repository.delete(pago_id)
    def _normalize(self, pago: tuple) -> dict:
        return {
            "id": pago[0],
            "idReservas": pago[1],
            "monto_pagado": pago[2],
            "metodo_pago": pago[3],
            "estado": pago[4],
            "fecha_pago": pago[5],
            "referencia": pago[6],
        }
    def confirmar_pago(self, pago_id: int) -> bool:
        from app.repositories.reserva_repository import ReservaRepository
        pago = self.repository.get_by_id(pago_id)
        if not pago:
            return False
        if pago[4] == "pagado":
            return True
        if pago[4] != "pendiente":
            return False
        reserva_repo = ReservaRepository()
        reserva = reserva_repo.get_by_id(pago[1])
        if not reserva or reserva[5] != "pendiente":
            return False
        monto_minimo = reserva[6] / 2
        if pago[2] < monto_minimo:
            return False
        self.repository.update_estado(pago_id, "pagado")
        reserva_repo.update_estado(pago[1], "confirmada")
        return True