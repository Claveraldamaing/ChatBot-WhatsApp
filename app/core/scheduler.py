from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.repositories.recordatorio_repository import RecordatorioRepository
from app.repositories.reserva_repository import ReservaRepository
from app.repositories.cliente_repository import ClienteRepository
import httpx
scheduler = AsyncIOScheduler()
BRIDGE_URL = "http://127.0.0.1:8001/send"
def iniciar_scheduler():
    scheduler.add_job(
        revisar_recordatorios,
        trigger="interval",
        minutes=1,
        id="revisar_recordatorios",
        replace_existing=True,
    )
    scheduler.start()
async def revisar_recordatorios():
    repo = RecordatorioRepository()
    reserva_repo = ReservaRepository()
    cliente_repo = ClienteRepository()
    pendientes = repo.get_pendientes()
    from datetime import datetime
    ahora = datetime.now()
    for r in pendientes:
        if r[4] and r[4] <= ahora:
            reserva = reserva_repo.get_by_id(r[1])
            if not reserva:
                continue
            cliente = cliente_repo.get_by_id(reserva[1])
            if not cliente:
                continue
            telefono = cliente[2]
            mensaje = r[3]
            try:
                async with httpx.AsyncClient() as client:
                    await client.post(BRIDGE_URL, json={"telefono": telefono, "texto": mensaje}, timeout=10)
                repo.update_estado(r[0], "enviado")
                print(f"[SCHEDULER] Recordatorio #{r[0]} enviado a {telefono}: {mensaje}")
            except Exception as e:
                print(f"[SCHEDULER] Error enviando recordatorio #{r[0]}: {e}")