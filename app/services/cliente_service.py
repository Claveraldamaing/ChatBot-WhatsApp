from app.repositories.cliente_repository import ClienteRepository
from app.schemas.cliente import ClienteCreate, ClienteResponse


class ClienteService:
    def __init__(self):
        self.repository = ClienteRepository()

    def list_clientes(self) -> list[ClienteResponse]:
        clientes = self.repository.get_all()
        return [ClienteResponse(**self._normalize(cliente)) for cliente in clientes]

    def get_cliente(self, cliente_id: int):
        cliente = self.repository.get_by_id(cliente_id)
        if cliente is None:
            return None
        return ClienteResponse(**self._normalize(cliente))

    def create_cliente(self, cliente_data: ClienteCreate):
        self.repository.create(cliente_data.model_dump())

    def update_cliente(self, cliente_id: int, cliente_data: ClienteCreate) -> bool:
        return self.repository.update(cliente_id, cliente_data.model_dump())

    def delete_cliente(self, cliente_id: int) -> bool:
        return self.repository.delete(cliente_id)

    def _normalize(self, cliente: tuple) -> dict:
        return {
            "id": cliente[0],
            "nombre": cliente[1],
            "telefono": cliente[2],
            "email": cliente[3],
            "fecha_registro": cliente[4],
        }
