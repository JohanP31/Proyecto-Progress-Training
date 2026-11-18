"""Patrón Facade: coordina el registro de un ingreso (HU-02 y HU-03).

Quien registra un ingreso solo llama a registrarIngreso(). La Facade
esconde los pasos: buscar al cliente y al empleado, revisar la
membresía (patrón State) y guardar el RegistroIngreso. No habla con la
base de datos: todo lo hace a través de los repositorios.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.ingreso import RegistroIngresoModel
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.ingreso_repository import IngresoRepository
from app.repositories.membresia_repository import MembresiaRepository
from app.repositories.usuario_repository import UsuarioRepository


class ClienteNoEncontradoError(Exception):
    """El cliente no existe."""


class EmpleadoNoEncontradoError(Exception):
    """El empleado que registra el ingreso no existe."""


class IngresoBloqueadoError(Exception):
    """HU-03: el cliente no tiene una membresía que permita el ingreso."""


class IngresoFacade:
    """Punto único para registrar el ingreso de un cliente."""

    def __init__(self, db: Session):
        # Sesión que necesita el repositorio de usuarios
        self.db = db
        # Repositorios que usa la Facade
        self.clientes = ClienteRepository(db)
        self.membresias = MembresiaRepository(db)
        self.ingresos = IngresoRepository(db)

    def registrarIngreso(
        self, cliente_id: int, empleado_id: int
    ) -> RegistroIngresoModel:
        """Valida la membresía (RN-01) y guarda el ingreso."""
        # 1. El cliente y el empleado deben existir
        if self.clientes.buscar_por_id(cliente_id) is None:
            raise ClienteNoEncontradoError(cliente_id)
        if not UsuarioRepository.existe_empleado(self.db, empleado_id):
            raise EmpleadoNoEncontradoError(empleado_id)

        # 2. Se revisa la membresía más reciente del cliente
        membresia = self.membresias.buscar_ultima(cliente_id)
        if membresia is None:
            raise IngresoBloqueadoError("El cliente no tiene membresía.")

        # 3. State: la membresía decide si deja entrar (HU-03)
        if not membresia.permitirIngreso():
            raise IngresoBloqueadoError("La membresía está vencida.")

        # 4. Se guarda el registro del ingreso
        registro = RegistroIngresoModel(
            fecha_hora=datetime.now(),
            tipo_ingreso=membresia.tipo,
            cliente_id=cliente_id,
            empleado_id=empleado_id,
        )
        return self.ingresos.guardar(registro)
