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
            telefono_real = cliente[2]
            respuesta_ia = self.ia_service.responder(texto, id_clientes)
            palabras_reserva = ['reserv', 'contrat', 'separ', 'cotiz', 'agend', 'dispon']
            if any(p in texto.lower() for p in palabras_reserva):
                if settings.ngrok_url:
                    respuesta_ia += (
                        f"\n\nPara reservar, ingresa aquí:\n"
                        f"{settings.ngrok_url}/formulario/reserva?telefono={telefono_real}"
                    )
            return respuesta_ia
        print(f"Cliente no registrado: {telefono}")
        if settings.ngrok_url:
            return (
                "Hola! Para poder atenderte mejor, primero necesitamos que te registres como cliente.\n"
                f"Regístrate aquí: {settings.ngrok_url}/formulario/cliente?telefono={telefono}"
            )
        return (
            "Hola! Para poder atenderte mejor, primero necesitamos que te registres como cliente. "
            "El formulario de registro no esta disponible por ahora."
        )
