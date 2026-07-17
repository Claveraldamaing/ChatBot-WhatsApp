import re
from app.services.ia_service import IAService
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.lid_map_repository import LidMapRepository
from app.core.config import settings


class WhatsAppService:
    def __init__(self):
        self.ia_service = IAService()
        self.cliente_repo = ClienteRepository()
        self.lid_map_repo = LidMapRepository()

    @staticmethod
    def _normalizar_telefono(tel: str) -> str:
        tel = re.sub(r'[^0-9]', '', tel)
        if len(tel) > 9:
            tel = tel[-9:]
        return tel

    def procesar_mensaje_local(self, telefono: str, texto: str) -> str | None:
        telefono_norm = self._normalizar_telefono(telefono)
        cliente = self.cliente_repo.get_by_telefono(telefono_norm)
        if cliente:
            id_clientes = cliente[0]
            telefono_real = cliente[2]
            respuesta_ia = self.ia_service.responder(texto, id_clientes)
            if respuesta_ia is None:
                respuesta_ia = "Lo siento, no pude procesar tu mensaje. Intenta de nuevo."
            palabras_reserva = ['reserv', 'contrat', 'separ', 'cotiz', 'agend', 'dispon']
            if any(p in texto.lower() for p in palabras_reserva):
                if settings.ngrok_url:
                    respuesta_ia += (
                        f"\n\nPara reservar, ingresa aqui:\n"
                        f"{settings.ngrok_url}/formulario/reserva?telefono={telefono_real}"
                    )
            return respuesta_ia

        telefono_limpio = re.sub(r'[^0-9]', '', telefono)
        if len(telefono_limpio) > 12:
            telefono_real = self.lid_map_repo.get_by_lid(telefono_limpio)
            if telefono_real:
                cliente = self.cliente_repo.get_by_telefono(telefono_real)
                if cliente:
                    id_clientes = cliente[0]
                    respuesta_ia = self.ia_service.responder(texto, id_clientes)
                    if respuesta_ia is None:
                        respuesta_ia = "Lo siento, no pude procesar tu mensaje. Intenta de nuevo."
                    return respuesta_ia

        print(f"Cliente no registrado: {telefono_norm}")
        if settings.ngrok_url:
            lid_param = f"&lid={telefono_limpio}" if len(telefono_limpio) > 12 else ""
            return (
                "Hola! Para poder atenderte mejor, primero necesitamos que te registres como cliente.\n"
                f"Registrate aqui: {settings.ngrok_url}/formulario/cliente?telefono={telefono_norm}{lid_param}"
            )
        return (
            "Hola! Para poder atenderte mejor, primero necesitamos que te registres como cliente. "
            "El formulario de registro no esta disponible por ahora."
        )
