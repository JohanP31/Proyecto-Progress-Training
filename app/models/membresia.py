from datetime import date

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.patterns.membresia_state import MembresiaVencida, MembresiaVigente


class MembresiaModel(Base):
    __tablename__ = "membresias"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    # El estado (vigente o vencida) no se guarda como texto:
    # lo calcula el patrón State a partir de fecha_fin.

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("ClienteModel", back_populates="membresias")
    pagos = relationship(
        "PagoModel", back_populates="membresia", cascade="all, delete-orphan"
    )

    # --- Patrón State ---

    @property
    def estado(self):
        """Devuelve el estado actual según la fecha de fin."""
        if self.fecha_fin >= date.today():
            return MembresiaVigente(self)
        return MembresiaVencida(self)

    @property
    def nombre_estado(self) -> str:
        """Nombre del estado para mostrarlo en la API."""
        return self.estado.nombre

    def permitirIngreso(self) -> bool:
        """Delega en el estado actual."""
        return self.estado.permitirIngreso()

    def renovar(self):
        """Delega en el estado actual: fecha de inicio de la renovación."""
        return self.estado.renovar()
