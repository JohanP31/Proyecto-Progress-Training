from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    documento = Column(String(50), unique=True, nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "usuario",
        "polymorphic_on": rol,
    }


class AdministradorModel(UsuarioModel):
    __tablename__ = "administradores"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    nivel_acceso = Column(String(50), nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "Administrador",
    }


class EmpleadoModel(UsuarioModel):
    __tablename__ = "empleados"

    id = Column(Integer, ForeignKey("usuarios.id"), primary_key=True)
    cargo = Column(String(50), nullable=False)
    salario = Column(Float, nullable=False)

    asistencias = relationship("AsistenciaModel", back_populates="empleado")

    __mapper_args__ = {
        "polymorphic_identity": "Empleado",
    }
