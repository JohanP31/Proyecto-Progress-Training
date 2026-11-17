"""Endpoints para la gestión de clientes (HU-01)."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.cliente import ClienteModel
from app.repositories.cliente_repository import (
    ClienteRepository,
    DocumentoDuplicadoError,
)
from app.schemas.cliente_schema import ClienteCrear, ClienteRespuesta

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post(
    "",
    response_model=ClienteRespuesta,
    status_code=status.HTTP_201_CREATED,
)
def registrar_cliente(datos: ClienteCrear, db: Session = Depends(get_db)):
    """HU-01: registra un cliente nuevo."""
    repositorio = ClienteRepository(db)
    try:
        return repositorio.crear(ClienteModel(**datos.model_dump()))
    except DocumentoDuplicadoError:
        # Convierte el error del repositorio en una respuesta HTTP
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un cliente con ese documento.",
        )


@router.get("/{cliente_id}", response_model=ClienteRespuesta)
def obtener_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Consulta un cliente por su id."""
    cliente = ClienteRepository(db).buscar_por_id(cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado.",
        )
    return cliente
