from app.repositories.paquete_repository import PaqueteRepository
from app.schemas.paquete import PaqueteCreate, PaqueteResponse
 
 
class PaqueteService:
    def __init__(self):
        self.repository = PaqueteRepository()
 
    def list_paquetes(self) -> list[PaqueteResponse]:
        paquetes = self.repository.get_all()
        return [PaqueteResponse(**self._normalize(p)) for p in paquetes]
 
    def get_paquete(self, paquete_id: int) -> PaqueteResponse | None:
        paquete = self.repository.get_by_id(paquete_id)
        if paquete is None:
            return None
        return PaqueteResponse(**self._normalize(paquete))
 
    def create_paquete(self, paquete_data: PaqueteCreate):
        self.repository.create(paquete_data.model_dump())
 
    def update_paquete(self, paquete_id: int, paquete_data: PaqueteCreate) -> bool:
        return self.repository.update(paquete_id, paquete_data.model_dump())
 
    def delete_paquete(self, paquete_id: int) -> bool:
        return self.repository.delete(paquete_id)
 
    def _normalize(self, paquete: tuple) -> dict:
        return {
            "id": paquete[0],
            "nombre_paquete": paquete[1],
            "descripcion": paquete[2],
            "precio": paquete[3],
            "estado": paquete[4],
        }
 