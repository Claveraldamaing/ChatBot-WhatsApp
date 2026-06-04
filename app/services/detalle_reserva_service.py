from app.repositories.detalle_reserva_repository import DetalleReservaRepository
from app.schemas.detalle_reserva import DetalleReservaCreate, DetalleReservaResponse


class DetalleReservaService:
    def __init__(self):
        self.repository = DetalleReservaRepository()

    def list_detalles(self) -> list[DetalleReservaResponse]:
        detalles = self.repository.get_all()
        return [DetalleReservaResponse(**self._normalize(d)) for d in detalles]

    def get_detalle(self, detalle_id: int) -> DetalleReservaResponse | None:
        detalle = self.repository.get_by_id(detalle_id)
        if detalle is None:
            return None
        return DetalleReservaResponse(**self._normalize(detalle))

    def list_by_reserva(self, reserva_id: int) -> list[DetalleReservaResponse]:
        detalles = self.repository.get_by_reserva(reserva_id)
        return [DetalleReservaResponse(**self._normalize(d)) for d in detalles]

    def create_detalle(self, data: DetalleReservaCreate):
        self.repository.create(data.model_dump())

    def update_detalle(self, detalle_id: int, data: DetalleReservaCreate) -> bool:
        return self.repository.update(detalle_id, data.model_dump())

    def delete_detalle(self, detalle_id: int) -> bool:
        return self.repository.delete(detalle_id)

    def _normalize(self, detalle: tuple) -> dict:
        return {
            "id": detalle[0],
            "idReservas": detalle[1],
            "idPaquetesEventos": detalle[2],
            "cantidad": detalle[3],
            "precio_unitario": detalle[4],
            "subtotal": detalle[5],
        }