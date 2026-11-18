"""Utilidades de seguridad: cifrado de contraseñas (RNF-03)."""

import hashlib
import secrets

# Cuántas veces se repite el cálculo. Más vueltas = más difícil de adivinar.
_ITERACIONES = 600_000


def hashear_contrasena(contrasena: str) -> str:
    """Devuelve la contraseña cifrada, lista para guardar en la base."""
    # La "sal" es un valor al azar: dos claves iguales quedan distintas
    sal = secrets.token_hex(16)
    clave = hashlib.pbkdf2_hmac(
        "sha256", contrasena.encode(), bytes.fromhex(sal), _ITERACIONES
    )
    # Se guarda todo junto para poder verificarla en el login
    return f"pbkdf2_sha256${_ITERACIONES}${sal}${clave.hex()}"
