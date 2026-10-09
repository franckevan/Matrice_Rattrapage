# Comment le mot de passe de la base est géré

Ce document présente le parcours du mot de passe PostgreSQL dans le module C4 et explique pourquoi il n'est pas intégré au code ni à l'image Docker.

## Le principe

Le mot de passe est conservé dans un fichier local : `c4/secrets/db_password.txt`. Compose le rend accessible aux conteneurs au démarrage. Le fichier reste sur la machine, n'est pas copié dans l'image et n'est pas envoyé sur GitHub.

## Son parcours dans le projet

1. **Le fichier local.** `c4/secrets/db_password.txt` contient le mot de passe de test sur une seule ligne. Git l'ignore grâce à `.gitignore`. Seul le modèle `c4/secrets/db_password.txt.example`, qui contient une valeur factice, est versionné.
2. **La configuration Compose.** Dans `compose.yaml`, `secrets` indique où se trouve le fichier. Les services `db` et `app` déclarent tous les deux qu'ils en ont besoin.
3. **Le montage dans les conteneurs.** Au démarrage, Docker rend le fichier accessible à `/run/secrets/db_password`. Il est monté à ce moment-là et ne fait donc pas partie de l'image.
4. **La connexion de PostgreSQL.** Le service `db` reçoit `POSTGRES_PASSWORD_FILE`, qui contient le chemin du fichier. À la première initialisation d'une base vide, PostgreSQL lit le mot de passe à cet emplacement pour créer l'utilisateur.
5. **La connexion de l'application.** Le service `app` reçoit de la même façon le chemin via `DB_PASSWORD_FILE`. La fonction `_password()` dans `c4/app/main.py` ouvre le fichier, lit le mot de passe et le transmet à `psycopg.connect`.

## Pourquoi le garder dans un fichier ?

- Un mot de passe écrit dans le `Dockerfile` pourrait être retrouvé dans les informations de l'image, par exemple avec `docker history` ou `docker image inspect`.
- Les variables d'environnement du conteneur sont consultables avec `docker inspect`. Ici, elles indiquent le chemin du fichier, pas le mot de passe.
- Le dépôt GitHub est public. Un secret qui y serait ajouté pourrait rester dans l'historique même après sa suppression.
- `.dockerignore` exclut `.env` et `secrets/` du contexte de construction, pour éviter qu'ils soient copiés dans l'image par erreur.
- Le fichier `.env` ne contient que des paramètres non sensibles : `POSTGRES_USER`, `POSTGRES_DB` et `APP_PORT`.

## Vérification

Dans le scénario 3, les recherches dans `docker history --no-trunc`, `docker image inspect`, les variables du conteneur et les fichiers de `/srv` ne trouvent pas le mot de passe. Une recherche témoin sur `useradd` renvoie bien un résultat, ce qui confirme que la recherche fonctionne. Dans le conteneur actif, `docker compose exec app env` affiche `DB_PASSWORD_FILE=/run/secrets/db_password`, et `ls -l /run/secrets` montre le fichier monté. Les commandes et leurs résultats sont détaillés dans [`c4/preuves/scenarios.md`](c4/preuves/scenarios.md).

## Ce qu'il faut garder en tête

- Le secret doit rester lisible par l'application pendant que le conteneur fonctionne. Une personne qui aurait accès au conteneur pourrait donc le lire. En production, il faudrait utiliser un gestionnaire de secrets dédié.
- Sous Docker Desktop pour Windows, le fichier monté apparaît avec des droits très larges (`rwxrwxrwx`).
- PostgreSQL lit ce mot de passe lors de l'initialisation d'une base vide. Modifier le fichier ensuite ne change pas le mot de passe d'une base déjà créée. Il faut alors le modifier dans PostgreSQL ou réinitialiser la base avec `docker compose down -v`, ce qui supprime aussi les données.
- Le fichier doit être en texte UTF-8, avec le mot de passe sur une seule ligne. La commande `echo >` de PowerShell peut produire un fichier UTF-16, que l'application ne lirait pas correctement.
