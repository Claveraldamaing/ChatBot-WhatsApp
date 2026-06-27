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
            respuesta_ia = self.ia_service.responder(texto, id_clientes)
            return respuesta_ia

        print(f"Cliente no registrado: {telefono}")
        if settings.form_cliente_url:
            return (
                "Hola! Para poder atenderte mejor, primero necesitamos que te registres como cliente.\n"
                f"Completa este formulario: {settings.form_cliente_url}"
            )

        return (
            "Hola! Para poder atenderte mejor, primero necesitamos que te registres como cliente. "
            "El formulario de registro no esta disponible por ahora."
        )
            
