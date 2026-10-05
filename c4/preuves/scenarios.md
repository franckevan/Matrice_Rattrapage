# Preuves C4 — scénarios exécutés

Environnement : Windows, PowerShell, Docker 29.3.1, Docker Compose v5.1.0, exécution du 5 octobre 2026.
Toutes les valeurs (mot de passe, données) sont factices. Les commandes se lancent depuis le dossier `c4/`.

## Commandes de base

```powershell
cp .env.example .env                                   # copy sous PowerShell
cp secrets\db_password.txt.example secrets\db_password.txt
docker compose up -d --build        # build + lancement
docker compose ps                   # inspection de l'état et de la santé
docker compose logs app             # journaux
docker compose exec app id          # inspection : utilisateur du conteneur
docker compose down                 # arrêt, volume conservé
docker compose down -v              # arrêt + suppression du volume
```

Constat après `up` : base `healthy`, puis application démarrée (`depends_on: service_healthy`).
`/health` : `200 {"status":"ok"}` ; `/ready` : `200 {"status":"ok","db":"up"}` ; `id` : `uid=10001(app)`.

## Scénario 1 — base non prête (conteneur démarré ≠ service disponible)

```powershell
docker compose down -v
docker compose up -d --no-deps app          # l'application seule, sans attendre la base
curl.exe -i http://127.0.0.1:8000/health    # 200 {"status":"ok"}
curl.exe -i http://127.0.0.1:8000/ready     # 503 {"status":"degraded","db":"down"}
1..40 | ForEach-Object {
  if ($_ -eq 5) { docker compose up -d db 2>&1 | Out-Null }
  curl.exe -s -o NUL -w '%{http_code} ' http://127.0.0.1:8000/ready
  Start-Sleep -Milliseconds 300 }
```

Résultat observé : 13 réponses `503` consécutives, puis 27 réponses `200`.
`/health` ne teste pas la base : il reste à `200` pendant que `/ready` indique `503`.
Fin : les deux services sont `healthy`.

## Scénario 2 — redémarrage préservant les données

```powershell
docker compose exec db psql -U matrice -d matrice -c "INSERT INTO seances_test (titre) VALUES ('donnee-persistante');"
docker compose down                          # conteneurs supprimés, volume matrice-c4_pgdata conservé
docker volume ls                             # matrice-c4_pgdata présent
docker compose up -d
docker compose exec db psql -U matrice -d matrice -c "SELECT * FROM seances_test;"
```

Résultat : la ligne `1 | donnee-persistante` est retrouvée après recréation des conteneurs.
Contraste : après `docker compose down -v` puis `up -d`, le `SELECT` renvoie `(0 rows)` (volume recréé vide).

## Scénario 3 — absence de secret dans l'image

```powershell
$secret = (Get-Content secrets\db_password.txt -Raw).Trim()
docker history --no-trunc matrice-c4-app | Select-String -SimpleMatch $secret          # aucune sortie
docker image inspect matrice-c4-app | Select-String -SimpleMatch $secret               # aucune sortie
docker run --rm --entrypoint env matrice-c4-app | Select-String -SimpleMatch $secret   # aucune sortie
docker run --rm --entrypoint grep matrice-c4-app -rF $secret /srv                      # aucune sortie
echo $LASTEXITCODE                                                                     # 1 (motif non trouvé)
docker history --no-trunc matrice-c4-app | Select-String -SimpleMatch "useradd"        # témoin : ligne trouvée
docker compose exec app env                  # DB_PASSWORD_FILE=/run/secrets/db_password (chemin, pas la valeur)
docker compose exec app ls -l /run/secrets   # le fichier est monté à l'exécution
```

Résultat : le secret est introuvable dans l'image. Le témoin `useradd` est trouvé, ce qui montre que la recherche fonctionne.
Limite : le secret reste lisible dans le conteneur en cours d'exécution.
Vérification Git : `git ls-files | Select-String "secrets|\.env$"` ne liste que `c4/secrets/db_password.txt.example` ; ni `.env` ni `db_password.txt` ne sont suivis par Git.

## Scénario 4 — restauration d'un jeu de test

```powershell
docker compose cp db/testset.sql db:/tmp/testset.sql
docker compose exec db psql -U matrice -d matrice -f /tmp/testset.sql
docker compose exec db pg_dump -U matrice -d matrice --clean --if-exists -f /tmp/sauvegarde.sql
docker compose cp db:/tmp/sauvegarde.sql preuves/sauvegarde.sql
docker compose exec db psql -U matrice -d matrice -c "DROP TABLE seances_test;"
docker compose exec db psql -U matrice -d matrice -c "SELECT * FROM seances_test;"   # ERROR: relation "seances_test" does not exist
docker compose cp preuves/sauvegarde.sql db:/tmp/restauration.sql
docker compose exec db psql -U matrice -d matrice -f /tmp/restauration.sql           # ... COPY 3 ...
docker compose exec db psql -U matrice -d matrice -c "SELECT * FROM seances_test;"
```

Résultat après restauration :

```
 id |      titre
----+------------------
  1 | React composants
  2 | Données et SQL
  3 | Revue de projet
(3 rows)
```

La sauvegarde `preuves/sauvegarde.sql` ne contient que des données fictives.
