from fastapi import APIRouter, HTTPException, status, Depends
from jose import jwt, JWTError
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioResponse,
    UsuarioLogin,
    TokenResponse,
    MessageResponse,
)
from app.services.usuario_service import UsuarioService, SECRET_KEY, ALGORITHM
router = APIRouter(prefix="/api", tags=["usuarios"])
service = UsuarioService()
def get_current_user(token: str = Depends(lambda: None)) -> dict:
    from fastapi import Header
    auth_header = Header(None, alias="Authorization")
    async def inner(authorization: str = Header(None, alias="Authorization")):
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token requerido",
            )
        token = authorization.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o expirado",
            )
    return inner
@router.post("/auth/login", response_model=TokenResponse)
def login(data: UsuarioLogin):
    usuario = service.authenticate(data.email, data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    token = service.create_token(usuario)
    return TokenResponse(access_token=token, usuario=usuario)
@router.get("/usuarios", response_model=list[UsuarioResponse])
def list_usuarios():
    return service.list_usuarios()
@router.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(usuario_id: int):
    usuario = service.get_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario
@router.post("/usuarios", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(data: UsuarioCreate):
    service.create_usuario(data)
    return MessageResponse(mensaje="Usuario creado correctamente")
@router.put("/usuarios/{usuario_id}", response_model=MessageResponse)
def update_usuario(usuario_id: int, data: UsuarioCreate):
    updated = service.update_usuario(usuario_id, data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return MessageResponse(mensaje="Usuario actualizado correctamente")
@router.delete("/usuarios/{usuario_id}", response_model=MessageResponse)
def delete_usuario(usuario_id: int):
    deleted = service.delete_usuario(usuario_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return MessageResponse(mensaje="Usuario eliminado correctamente")