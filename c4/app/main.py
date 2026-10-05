"""Micro-application C4 : GET /health (processus vivant) et GET /ready (base joignable)."""
import os

import psycopg
from fastapi import FastAPI, Response

app = FastAPI(title="C4 micro-app")


def _password():
    # Le secret est lu depuis un fichier monté (compose secrets), jamais depuis l'image.
    path = os.getenv("DB_PASSWORD_FILE")
    if path:
        with open(path, encoding="utf-8") as f:
            return f.read().strip()
    return os.getenv("DB_PASSWORD", "")


def _conn_params():
    return {
        "host": os.getenv("DB_HOST", "db"),  # nom du service Compose = DNS interne
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "matrice"),
        "user": os.getenv("DB_USER", "matrice"),
        "password": _password(),
        "connect_timeout": 2,
    }


@app.get("/health")
def health():
    """Ne teste PAS la base : prouve seulement que le processus répond."""
    return {"status": "ok"}


@app.get("/ready")
def ready(response: Response):
    """Teste réellement la connexion à PostgreSQL (SELECT 1)."""
    try:
        with psycopg.connect(**_conn_params()) as conn:
            conn.execute("SELECT 1")
        return {"status": "ok", "db": "up"}
    except Exception:
        response.status_code = 503
        return {"status": "degraded", "db": "down"}
