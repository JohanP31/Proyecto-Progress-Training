"""Endpoints para el registro y consulta de usuarios internos."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import hashear_contrasena
from app.models.usuario import AdministradorModel, EmpleadoModel
from app.repositories.usuario_repository import (
    UsuarioDuplicadoError,
    UsuarioRepository,
)
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios y Personal"])


@router.post(
    "/",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un usuario interno (Administrador o Empleado)."""
    if UsuarioRepository.obtener_por_correo(
        db, datos.correo
    ) or UsuarioRepository.obtener_por_documento(db, datos.documento):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo o documento.",
        )

    campos_comunes = datos.model_dump(
        exclude={"nivel_acceso", "cargo", "salario"}
    )
    # Nunca se guarda la contraseña tal cual: se guarda cifrada (RNF-03)
    campos_comunes["contrasena"] = hashear_contrasena(datos.contrasena)
    if datos.rol == "Administrador":
        nuevo_usuario = AdministradorModel(
            **campos_comunes,
            nivel_acceso=datos.nivel_acceso,
        )
    else:
        nuevo_usuario = EmpleadoModel(
            **campos_comunes,
            cargo=datos.cargo,
            salario=datos.salario,
        )

    try:
        return UsuarioRepository.crear_usuario(db, nuevo_usuario)
    except UsuarioDuplicadoError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo o documento.",
        ) from None


@router.get("/empleados", response_model=list[UsuarioResponse])
def listar_empleados(db: Session = Depends(get_db)):
    """Devuelve todos los usuarios que son empleados."""
    return UsuarioRepository.listar_empleados(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Consulta los detalles de un usuario interno por su ID único."""
    usuario = UsuarioRepository.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado.",
        )
    return usuario
