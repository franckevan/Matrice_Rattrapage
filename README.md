# Rattrapage MATRiCE (WEB2) — Franck YAPI

Trois modules indépendants : **C3** (cybersécurité / monitoring IA), **C4** (Docker & Compose) et **I2** (normalisation et dashboarding).
Dépôt public : https://github.com/franckevan/Matrice_Rattrapage

| Module | Dossier | Contenu |
|---|---|---|
| C3 | `c3/` | dossier d'analyse (PDF), règles d'alerte et journalisation sans secret en Python, 16 tests |
| C4 | `c4/` | micro-application FastAPI + PostgreSQL, `Dockerfile`, `compose.yaml`, preuves des 4 scénarios |
| I2 | `i2/` | pipeline Python de normalisation, indicateurs, dashboard HTML, 13 tests |

Documents transverses : [`JUSTIFICATIONS.md`](JUSTIFICATIONS.md) (choix, alternatives, preuves, limites) et [`SOURCES_IA.md`](SOURCES_IA.md) (usages de l'IA).

## Prérequis
- **Python 3.10 ou plus** pour C3 et I2 (bibliothèque standard uniquement, aucune installation). Testé avec Python 3.14 sous Windows.
- **Docker Desktop** (Docker Engine et Compose v2 ou plus) pour C4. Testé avec Docker 29.3.1 et Compose v5.1.0.
- PowerShell. Sous Linux/macOS, remplacer `copy` par `cp` et `curl.exe` par `curl`.

## Lancer et tester chaque module
Toutes les commandes Python se lancent **depuis la racine du dépôt** (le dossier qui contient `c3/`, `c4/` et `i2/`).

### I2 — normalisation et dashboard
```powershell
python -m i2.generate_dataset        # recrée i2/data/seances.ndjson (12 lignes)
python -m i2                         # normalise, calcule, écrit i2/out/
start i2\out\dashboard.html          # ouvre le dashboard dans le navigateur
python -m unittest discover -s i2/tests -t . -v   # 13 tests
```

### C3 — alertes et journalisation sans secret
```powershell
python -m c3                         # 3 alertes sur c3/data/journal.log
python -m unittest discover -s c3/tests -t . -v   # 16 tests
```
Le dossier d'analyse (risques, frontières de confiance, règle commentée, runbook) est `c3/C3_dossier_cybersecurite.pdf`.

### C4 — Docker & Compose
```powershell
cd c4
copy .env.example .env
copy secrets\db_password.txt.example secrets\db_password.txt   # puis y mettre un mot de passe factice
docker compose up -d --build
docker compose ps
curl.exe -i http://127.0.0.1:8000/health
curl.exe -i http://127.0.0.1:8000/ready
docker compose down
```
Le détail des commandes et des scénarios est dans [`c4/README.md`](c4/README.md) et [`c4/preuves/scenarios.md`](c4/preuves/scenarios.md).

## Structure utile
```
c3/  C3_dossier_cybersecurite.pdf  detect.py  redact.py  data/  tests/
c4/  Dockerfile  compose.yaml  .env.example  app/  db/  secrets/  preuves/
i2/  normalize.py  metrics.py  dashboard.py  generate_dataset.py  data/  out/  tests/
```

## Sécurité du dépôt
Aucun secret réel n'est versionné : `.env` et `c4/secrets/db_password.txt` sont ignorés par Git, seuls leurs modèles `.example` (valeurs factices) sont présents. Aucune donnée personnelle réelle n'est utilisée.
