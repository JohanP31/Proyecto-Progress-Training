"""Servicio para renovar membresías (HU-04).

Coordina los pasos de la renovación usando los patrones State y
Factory Method. No habla con la base de datos: eso lo hacen los
repositorios.
"""

from datetime import date

from sqlalchemy.orm import Session

from app.models.membresia import MembresiaModel
from app.models.pago import PagoModel
from app.patterns.membresia_factory import MembresiaFactory
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.membresia_repository import MembresiaRepository
from app.repositories.pago_repository import PagoRepository


class ClienteNoEncontradoError(Exception):
    """Se lanza cuando el cliente no existe."""


class MembresiaService:
    """Reglas para renovar la membresía de un cliente."""

    def __init__(self, db: Session):
        # Repositorios que usa el servicio
        self.clientes = ClienteRepository(db)
        self.membresias = MembresiaRepository(db)
        self.pagos = PagoRepository(db)

    def renovar(
        self, cliente_id: int, tipo: str, metodo_pago: str
    ) -> tuple[MembresiaModel, PagoModel]:
        """Crea la nueva membresía del cliente y registra su pago."""
        # 1. El cliente debe existir
        if self.clientes.buscar_por_id(cliente_id) is None:
            raise ClienteNoEncontradoError(cliente_id)

        # 2. State: la membresía actual decide desde cuándo se renueva.
        #    Si el cliente nunca ha tenido membresía, empieza hoy.
        ultima = self.membresias.buscar_ultima(cliente_id)
        fecha_inicio = ultima.renovar() if ultima else date.today()

        # 3. Factory Method: arma la membresía según su tipo
        membresia = MembresiaFactory.crear(tipo, fecha_inicio)
        membresia.cliente_id = cliente_id
        membresia = self.membresias.crear(membresia)

        # 4. Se registra el pago por el valor de la membresía
        pago = PagoModel(
            fecha=date.today(),
            monto=membresia.valor,
            metodo_pago=metodo_pago,
            concepto=f"Membresía {tipo}",
            membresia_id=membresia.id,
        )
        pago = self.pagos.crear(pago)
        return membresia, pago

    def consultar_actual(self, cliente_id: int) -> MembresiaModel | None:
        """Devuelve la última membresía del cliente, o None."""
        if self.clientes.buscar_por_id(cliente_id) is None:
            raise ClienteNoEncontradoError(cliente_id)
        return self.membresias.buscar_ultima(cliente_id)
