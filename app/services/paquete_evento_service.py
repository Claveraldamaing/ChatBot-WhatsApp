from app.repositories.paquete_evento_repository import PaqueteEventoRepository
from app.schemas.paquete_evento import PaqueteEventoCreate, PaqueteEventoResponse


class PaqueteEventoService:
    def __init__(self):
        self.repository = PaqueteEventoRepository()

    def list_paquetes_eventos(self) -> list[PaqueteEventoResponse]:
        registros = self.repository.get_all()
        return [PaqueteEventoResponse(**self._normalize(r)) for r in registros]

    def get_paquete_evento(self, paquete_evento_id: int) -> PaqueteEventoResponse | None:
        registro = self.repository.get_by_id(paquete_evento_id)
        if registro is None:
            return None
        return PaqueteEventoResponse(**self._normalize(registro))

    def list_by_evento(self, evento_id: int) -> list[PaqueteEventoResponse]:
        registros = self.repository.get_by_evento(evento_id)
        return [PaqueteEventoResponse(**self._normalize(r)) for r in registros]

    def create_paquete_evento(self, data: PaqueteEventoCreate):
        self.repository.create(data.model_dump())

    def delete_paquete_evento(self, paquete_evento_id: int) -> bool:
        return self.repository.delete(paquete_evento_id)

    def _normalize(self, registro: tuple) -> dict:
        return {
            "id": registro[0],
            "idPaquetes": registro[1],
            "idEventos": registro[2],
        }