from openai import OpenAI

from app.core.config import settings
from app.repositories.mensajes_ia_repository import MensajesIARepository
from app.repositories.paquete_repository import PaqueteRepository
from app.repositories.evento_repository import EventoRepository
from app.repositories.cliente_repository import ClienteRepository


client = OpenAI(
    api_key=settings.openai_api_key
)


class IAService:

    def __init__(self):
        self.mensajes_repository = MensajesIARepository()
        self.paquete_repository = PaqueteRepository()
        self.evento_repository = EventoRepository()
        self.cliente_repository = ClienteRepository()

    def responder(self, texto: str, id_clientes: int) -> str:

        # Obtener historial anterior desde PostgreSQL
        historial = self.mensajes_repository.get_by_cliente(id_clientes, limit=8)

        # Como viene ordenado DESC, lo invertimos para leerlo en orden cronológico
        historial = list(reversed(historial))

        historial_texto = "\n".join(
            [
                f"{mensaje[0]}: {mensaje[1]}"
                for mensaje in historial
            ]
        )
        paquetes = self.paquete_repository.get_activos_para_ia()
        eventos = self.evento_repository.get_all_para_ia()
        cliente = self.cliente_repository.get_by_id(id_clientes)

        if cliente:
            cliente_texto = f"""
- ID: {cliente[0]}
- Nombre: {cliente[1]}
- Telefono: {cliente[2]}
- Email: {cliente[3] or "No registrado"}
"""
        else:
            cliente_texto = "No se encontro informacion del cliente registrado."

        eventos_texto = "\n".join(
        [
        f"- {evento[0]}: {evento[1]}"
        for evento in eventos
        ]
        )

        paquetes_texto = "\n".join(
         [
        f"- {paquete[0]}: {paquete[1]} | Precio: S/ {paquete[2]} | Estado: {paquete[3]}"
        for paquete in paquetes
         ]
         )

        respuesta = client.responses.create(
            model="gpt-4o-mini",
            input=f"""
Eres un chatbot inteligente especializado en la atención y gestión de eventos en Trujillo.

OBJETIVO:
Ayudar a los clientes a consultar información, solicitar cotizaciones y realizar reservas de eventos mediante WhatsApp.

CLIENTE REGISTRADO:
{cliente_texto}

EVENTOS DISPONIBLES EN BASE DE DATOS:
{eventos_texto}

PAQUETES DISPONIBLES EN BASE DE DATOS:
{paquetes_texto}

COMPORTAMIENTO:
- Responde de forma amable, profesional y breve.
- Mantén un tono cordial y orientado al cliente.
- No inventes precios ni disponibilidad.
- Si el usuario pregunta por paquetes o precios, usa únicamente la información de PAQUETES DISPONIBLES EN BASE DE DATOS.
- Si no existe un paquete relacionado en la base de datos, indica que un asesor debe confirmar la información.
- Si no tienes información suficiente, solicita más datos.
- Siempre busca ayudar al cliente a continuar con el proceso de reserva.
- Usa el historial de conversación para no repetir preguntas que el cliente ya respondió.
- Si el cliente ya indicó un dato, recuérdalo y continúa solicitando solo los datos faltantes.

- Este cliente ya esta registrado en la base de datos.
- No envies el Formulario de Cliente ni FORM_CLIENTE_URL a clientes registrados.
- Si el nombre del cliente esta disponible, saludalo por su nombre de forma natural.
- Usa unicamente los datos del cliente mostrados en CLIENTE REGISTRADO.
- No inventes nombre, telefono, email ni otros datos del cliente.
- Solo envia el Formulario de Reserva cuando el cliente quiera reservar, cotizar, agendar o consultar disponibilidad.

REGLAS IMPORTANTES:

1. CONSULTAS GENERALES

Si el cliente solicita informacion general, paquetes, servicios o desea conocer mas sobre la empresa, responde la consulta usando la informacion disponible. No envies el formulario de registro porque este cliente ya esta registrado.

2. RESERVAS

Si el cliente menciona palabras como:
- reservar
- contratar
- separar fecha
- cotizar
- agendar
- disponibilidad
- evento
- cumpleaños
- show infantil

Debes solicitar los siguientes datos:
- Fecha del evento.
- Tipo de evento.
- Cantidad de invitados.
- Ubicación.

Además, comparte inmediatamente el formulario de reserva.

Formulario de Reserva:
{settings.form_reserva_url}

3. COTIZACIONES

Si el cliente solicita precios o cotizaciones:
- No inventes montos.
- Explica que la cotización depende de la fecha, ubicación, duración, tipo de evento y cantidad de invitados.
- Solicita la información necesaria.
- Comparte el formulario de reserva.

4. DISPONIBILIDAD

Si preguntan por disponibilidad:
- Indica que se debe validar la fecha.
- Solicita la fecha del evento si aún no la indicó.
- Comparte el formulario de reserva.

5. FORMULARIOS

Siempre que compartas un formulario, muestra el enlace completo para que el cliente pueda acceder directamente.

6. USO DEL HISTORIAL

El historial muestra los mensajes anteriores de este cliente.
Debes usarlo para entender el contexto.
Por ejemplo:
- Si el cliente primero dijo que quería reservar.
- Luego dice "será para 50 invitados".
Debes entender que sigue hablando de la misma reserva.

HISTORIAL DE LA CONVERSACIÓN:
{historial_texto}

NUEVO MENSAJE DEL CLIENTE:
{texto}
"""
        )

        respuesta_texto = respuesta.output_text

        # Guardar mensaje del cliente en PostgreSQL
        self.mensajes_repository.create({
            "idClientes": id_clientes,
            "rol": "cliente",
            "contenido": texto,
            "tipo": "entrada",
            "estado": "activo",
            "tiene_reserva": False
        })

        # Guardar respuesta de la IA en PostgreSQL
        self.mensajes_repository.create({
            "idClientes": id_clientes,
            "rol": "asistente",
            "contenido": respuesta_texto,
            "tipo": "respuesta",
            "estado": "activo",
            "tiene_reserva": False
        })

        return respuesta_texto
