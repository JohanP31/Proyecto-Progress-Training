"""Patrón State: estados de una membresía (vigente o vencida).

La membresía no guarda su estado como texto. Según su fecha_fin se
crea el estado que corresponde, y la membresía le delega las
decisiones: si permite el ingreso y desde cuándo empieza la renovación.
"""

from abc import ABC, abstractmethod
from datetime import date, timedelta


class EstadoMembresia(ABC):
    """Lo que todo estado de membresía debe saber responder."""

    # Nombre que se muestra en la API
    nombre = ""

    def __init__(self, membresia):
        # Membresía a la que pertenece este estado
        self.membresia = membresia

    @abstractmethod
    def permitirIngreso(self) -> bool:
        """Dice si el cliente puede entrar al gimnasio (RN-01)."""

    @abstractmethod
    def renovar(self) -> date:
        """Dice desde qué fecha empieza la nueva membresía."""


class MembresiaVigente(EstadoMembresia):
    """La membresía todavía no ha vencido."""

    nombre = "Vigente"

    def permitirIngreso(self) -> bool:
        return True

    def renovar(self) -> date:
        # Empieza al día siguiente del fin: no se pierden días pagados
        return self.membresia.fecha_fin + timedelta(days=1)


class MembresiaVencida(EstadoMembresia):
    """La membresía ya venció."""

    nombre = "Vencida"

    def permitirIngreso(self) -> bool:
        # HU-03: con la membresía vencida se bloquea el ingreso
        return False

    def renovar(self) -> date:
        # Ya venció: la nueva membresía empieza hoy
        return date.today()
