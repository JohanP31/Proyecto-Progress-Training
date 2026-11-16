from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class MembresiaModel(Base):
    __tablename__ = "membresias"

    id = Column(Integer, primary_key=True, index=True)
    tipo = Column(String(50), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    valor = Column(Float, nullable=False)
    estado = Column(String(20), nullable=False)

    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("ClienteModel", back_populates="membresias")
    pagos = relationship(
        "PagoModel", back_populates="membresia", cascade="all, delete-orphan"
    )
