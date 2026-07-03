from datetime import datetime
from pydantic import BaseModel
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    rol: str = "admin"
    estado: str = "activo"
class UsuarioCreate(UsuarioBase):
    password: str
class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime | None = None
    class Config:
        from_attributes = True
class UsuarioLogin(BaseModel):
    email: str
    password: str
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario: UsuarioResponse
class MessageResponse(BaseModel):
    mensaje: str