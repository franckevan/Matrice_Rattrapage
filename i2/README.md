# Module I2 — Normalisation et dashboarding

Python 3.10+ ; **aucune dépendance** (bibliothèque standard uniquement).

## Commandes (depuis la racine du dépôt)
```bash
python -m i2.generate_dataset   # recrée i2/data/seances.ndjson (12 lignes)
python -m i2                    # normalise, calcule, écrit i2/out/*
python -m unittest discover -s i2/tests -t . -v   # tests
```
Ouvrir `i2/out/dashboard.html` dans un navigateur.

## Structure
- `normalize.py` : validation, normalisation, déduplication
- `metrics.py` : indicateurs
- `dashboard.py` : rapport HTML (graphiques SVG inline)
- `generate_dataset.py` : recrée le jeu de données de l'énoncé
- `out/` : sorties (données normalisées, rejets motivés, doublons, métriques, dashboard)
