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

    def create_reserva(self, data: ReservaCreate):
        self.repository.create(data.model_dump())

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