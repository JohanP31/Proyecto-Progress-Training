from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.usuario import AdministradorModel, EmpleadoModel
from app.repositories.usuario_repository import (
    UsuarioDuplicadoError,
    UsuarioRepository,
)
from app.schemas.usuario_schema import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios y Personal"])


@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(datos: UsuarioCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario interno (Administrador o Empleado) en el sistema."""
    if UsuarioRepository.obtener_por_correo(
        db, datos.correo
    ) or UsuarioRepository.obtener_por_documento(db, datos.documento):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un usuario con ese correo o documento.",
        )

    campos_comunes = datos.model_dump(exclude={"nivel_acceso", "cargo", "salario"})
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


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Consulta los detalles de un usuario interno por su ID único."""
    usuario = UsuarioRepository.obtener_por_id(db, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado."
        )
    return usuario


"""Para la creacion de usuarios, administradores deben tener el nivel de acceso 'TOTAL' y no se debe
escribir nada en cargo ni salario, mientras que los empleados deben tener un cargo y salario y no se debe escribir nada en nivel de acceso.

ej. 
  "nombre": "Juan camilo R",
  "documento": "10182455213",
  "telefono": "321679",
  "correo": "user@example.com",
  "contrasena": "123456",
  "rol": "Administrador",
  "nivel_acceso": "TOTAL"

ej.2
  "nombre": "Luis Gómez",
  "documento": "987654321",
  "telefono": "3107654321",
  "correo": "luis@example.com",
  "contrasena": "clave-de-prueba",
  "rol": "Empleado",
  "cargo": "Entrenador",
  "salario": 2500000

"""
