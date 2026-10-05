# Module C4 — Docker & Compose

Micro-application FastAPI (`GET /health` → `200 {"status":"ok"}`) avec une base PostgreSQL 16, dans deux conteneurs reliés par un réseau privé. Le module ne dépend pas du backend MATRiCE.

## Prérequis
- Docker Desktop (Docker Engine et Compose v2 ou plus), PowerShell.
- Testé avec Docker 29.3.1 et Compose v5.1.0 sous Windows. Non testé sous Linux/macOS.

## Préparation (valeurs factices, rien de réel n'est versionné)
Depuis le dossier `c4/` :
```powershell
copy .env.example .env
copy secrets\db_password.txt.example secrets\db_password.txt
```
Ouvrir ensuite `secrets\db_password.txt` avec un éditeur de texte et y mettre un mot de passe factice, sur une seule ligne. Ne pas utiliser `echo >` : PowerShell écrirait le fichier en UTF-16 et la lecture échouerait. `.env` et `db_password.txt` sont ignorés par Git.

## Commandes
```powershell
docker compose up -d --build         # construire l'image et lancer les deux services
docker compose ps                    # état et santé (db puis app doivent être "healthy")
docker compose logs app              # journaux de l'application
docker compose exec app id           # inspection : utilisateur du conteneur (uid=10001)
curl.exe -i http://127.0.0.1:8000/health
curl.exe -i http://127.0.0.1:8000/ready
docker compose down                  # arrêt, le volume est conservé
docker compose down -v               # arrêt + suppression du volume (les données sont perdues)
```
Sous Linux/macOS : `cp` à la place de `copy`, `curl` à la place de `curl.exe`, et le fichier de secret doit être lisible par l'utilisateur 10001 du conteneur.

## Deux routes, deux questions différentes
- `/health` répond `200` tant que le processus tourne. **Elle ne teste pas la base.**
- `/ready` tente une connexion à PostgreSQL (`SELECT 1`) : `200` si la base répond, `503` sinon.

Le healthcheck Docker de l'application appelle `/health`. La disponibilité réelle de la base est donc vérifiée séparément, par `/ready` et par le healthcheck `pg_isready` du service `db`.

## Scénarios et preuves
Les quatre scénarios (base non prête, redémarrage préservant les données, absence de secret dans l'image, restauration d'un jeu de test) sont décrits avec leurs commandes et leurs résultats dans [`preuves/scenarios.md`](preuves/scenarios.md). La sauvegarde utilisée pour la restauration est `preuves/sauvegarde.sql` (données fictives).

## Structure
```
c4/
  Dockerfile            image de l'application (utilisateur non privilégié, healthcheck)
  compose.yaml          services app et db, réseau, volume, secrets, healthchecks
  requirements.txt      dépendances Python figées
  .env.example          variables factices
  app/main.py           micro-application (/health, /ready)
  db/init/01-schema.sql schéma créé au premier démarrage de la base
  db/testset.sql        jeu de test fictif
  secrets/db_password.txt.example   modèle de secret factice
  preuves/              scénarios et sauvegarde
```
