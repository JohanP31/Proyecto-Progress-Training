from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class PagoModel(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    fecha = Column(Date, nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    concepto = Column(String(100), nullable=False)

    membresia_id = Column(Integer, ForeignKey("membresias.id"), nullable=False)

    membresia = relationship("MembresiaModel", back_populates="pagos")
