from app.repositories.evento_repository import EventoRepository
from app.schemas.evento import EventoCreate, EventoResponse


class EventoService:
    def __init__(self):
        self.repository = EventoRepository()

    def list_eventos(self) -> list[EventoResponse]:
        eventos = self.repository.get_all()
        return [EventoResponse(**self._normalize(e)) for e in eventos]

    def get_evento(self, evento_id: int) -> EventoResponse | None:
        evento = self.repository.get_by_id(evento_id)
        if evento is None:
            return None
        return EventoResponse(**self._normalize(evento))

    def create_evento(self, data: EventoCreate):
        self.repository.create(data.model_dump())

    def update_evento(self, evento_id: int, data: EventoCreate) -> bool:
        return self.repository.update(evento_id, data.model_dump())

    def delete_evento(self, evento_id: int) -> bool:
        return self.repository.delete(evento_id)

    def _normalize(self, evento: tuple) -> dict:
        return {
            "id": evento[0],
            "nombre": evento[1],
            "descripcion": evento[2],
        }