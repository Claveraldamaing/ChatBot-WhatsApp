from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(tags=["formularios"])
@router.get("/formulario/cliente", response_class=HTMLResponse)
async def formulario_cliente(telefono: str):
    html_path = Path(__file__).parent.parent.parent / "templates" / "formulario_clientes.html"
    html = html_path.read_text(encoding="utf-8")
    return html