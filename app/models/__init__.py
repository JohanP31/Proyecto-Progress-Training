"""Modelos ORM de la aplicación."""

# Se importan todos los modelos para que SQLAlchemy los conozca
# y pueda crear las tablas y sus relaciones.
from app.models.usuario import UsuarioModel, AdministradorModel, EmpleadoModel
from app.models.cliente import ClienteModel
from app.models.membresia import MembresiaModel
from app.models.pago import PagoModel
from app.models.ingreso import RegistroIngresoModel
from app.models.asistencia import AsistenciaModel
from app.models.producto import ProductoModel, VentaProductoModel
from app.models.maquina import MaquinaModel, MantenimientoModel
