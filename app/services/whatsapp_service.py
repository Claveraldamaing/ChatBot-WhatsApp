import time
from app.services.ia_service import IAService
from app.repositories.cliente_repository import ClienteRepository
from app.core.config import settings


class WhatsAppService:

    def __init__(self):
        self.ia_service = IAService()
        self.cliente_repo = ClienteRepository()


    def procesar_mensaje_local(self, telefono: str, texto: str) -> str | None:
        cliente = self.cliente_repo.get_by_telefono(telefono)
        if cliente:
            id_clientes = cliente[0]
            print(f"Cliente existente: ID {id_clientes}")
        else:
            id_clientes = self.cliente_repo.create_simple(telefono)
            print(f"Nuevo cliente creado con ID: {id_clientes}")
        respuesta_ia = self.ia_service.responder(texto, id_clientes)
        return respuesta_ia
            