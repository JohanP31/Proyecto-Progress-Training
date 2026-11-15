"""Punto de entrada de la API FastAPI."""

from fastapi import FastAPI

app = FastAPI(title="Progress Training API")


@app.get("/", tags=["health"])
def health_check() -> dict[str, str]:
    """Confirma que la API está disponible."""
    return {"status": "ok"}
