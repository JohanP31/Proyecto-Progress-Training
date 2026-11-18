"""Acceso a datos de clientes."""

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.cliente import ClienteModel


class DocumentoDuplicadoError(Exception):
    """Se lanza cuando ya existe un cliente con el mismo documento."""


class ClienteRepository:
    """Guarda y busca clientes. Es lo único que habla con la tabla."""

    def __init__(self, db: Session):
        # Sesión de base de datos que recibe desde el router
        self.db = db

    def crear(self, cliente: ClienteModel) -> ClienteModel:
        """Guarda un cliente nuevo y lo devuelve con su id."""
        self.db.add(cliente)
        try:
            self.db.commit()
        except IntegrityError:
            # La columna documento es única: la base rechaza el repetido
            self.db.rollback()
            raise DocumentoDuplicadoError(cliente.documento)
        # Recarga el cliente para traer el id y el estado por defecto
        self.db.refresh(cliente)
        return cliente

    def buscar_por_id(self, cliente_id: int) -> ClienteModel | None:
        """Devuelve el cliente con ese id, o None si no existe."""
        return self.db.get(ClienteModel, cliente_id)

    def listar(self) -> list[ClienteModel]:
        """Devuelve todos los clientes ordenados por nombre."""
        return (
            self.db.query(ClienteModel)
            .order_by(ClienteModel.nombre)
            .all()
        )
