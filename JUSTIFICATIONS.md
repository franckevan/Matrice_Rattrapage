# Mes choix pour les trois modules

Voici les principaux choix faits pour I2, C4 et C3, avec les raisons derrière ces choix et les limites à garder en tête.

## I2 — Normalisation et dashboard

### Choix

- J'ai utilisé Python sans dépendance externe. Le projet peut ainsi être lancé sans installation supplémentaire.
- Je valide chaque ligne avant de vérifier les doublons, comme le demande le sujet. Un identifiant invalide n'est donc pas enregistré et ne peut pas empêcher le traitement d'une ligne valide qui porte le même identifiant.
- Pour les dates, je vérifie d'abord leur format, puis `datetime.date` permet de rejeter les dates impossibles, comme `2026-02-30`.
- Les correspondances pour les périodes, les statuts, les groupes et les modes sont regroupées dans des dictionnaires. Les règles métier sont ainsi plus faciles à retrouver et à modifier.
- Le dashboard utilise du SVG directement dans la page, sans CDN : il reste consultable hors ligne.

J'aurais pu utiliser pandas, mais il aurait ajouté une dépendance pour un jeu de seulement 12 lignes et aurait rendu les règles moins visibles. J'ai aussi écarté Chart.js, qui aurait nécessité une ressource externe.

### Hypothèses sur les données

- La ligne `bad1` est rejetée parce que son titre est vide. Son mode AUTO, son formateur `null` et son statut `proposed` respectent les règles.
- Les séances `proposed` avec un formateur sont incluses dans le calcul des heures par formateur (`s04` pour t2 et `s05` pour t3). Seules les séances AUTO sont exclues.

### Résultats et limites

Les fichiers de `i2/out/` contiennent les données normalisées, les rejets motivés, les doublons, les métriques et le dashboard. Les 13 tests couvrent aussi le cas d'un jeu vide et celui d'un dénominateur nul. Le traitement donne 6 séances acceptées, 4 rejets et 2 doublons. Les heures par formateur sont de 7 h, 7 h et 3,5 h ; les heures-apprenant sont de 14 h pour A et B ; le taux de confirmation est de 3/5, soit 60 %.

La validation du domaine vérifie seulement qu'il s'agit d'un texte non vide. La durée de 3,5 h est une constante, et le jeu de données reste très petit.

## C4 — Docker et Compose

### Choix

- La base et l'application communiquent sur un réseau privé. La base ne publie pas de port ; l'application est accessible uniquement sur `127.0.0.1`.
- L'application trouve PostgreSQL avec le nom de service `db`.
- Les versions de PostgreSQL (`postgres:16.4-alpine`), Python (`python:3.12.7-slim`) et des dépendances sont fixées pour que les constructions soient plus faciles à reproduire.
- Le conteneur de l'application tourne avec un utilisateur non privilégié (uid 10001). Son système de fichiers est en lecture seule, ses capacités sont retirées et l'escalade de privilèges est désactivée.
- Le mot de passe passe par un fichier déclaré comme secret Compose. `POSTGRES_PASSWORD_FILE` et `DB_PASSWORD_FILE` donnent aux services le chemin du fichier, pas sa valeur dans une variable d'environnement.
- `/health` vérifie que le processus répond. `/ready` vérifie aussi la connexion à PostgreSQL avec `SELECT 1`, et PostgreSQL possède son propre healthcheck basé sur `pg_isready`.
- Avec `depends_on: service_healthy`, l'application attend que la base soit prête avant de démarrer.
- Le volume `pgdata` conserve les données après l'arrêt des conteneurs.

J'ai retenu PostgreSQL parce qu'il correspond au reste du projet et suffit pour ce besoin. Un mot de passe dans une variable d'environnement serait plus facile à exposer avec `docker inspect`. J'ai aussi abandonné le script d'automatisation des scénarios, car je ne l'avais pas testé ; j'ai préféré exécuter les commandes manuellement et vérifier leurs résultats.

### Scénarios vérifiés

Les résultats détaillés figurent dans [`c4/preuves/scenarios.md`](c4/preuves/scenarios.md). J'ai exécuté les quatre scénarios sous Windows avec Docker 29.3.1 et Compose v5.1.0 :

1. Quand la base n'est pas prête, `/health` renvoie 200 tandis que `/ready` renvoie 503. Pendant le démarrage de la base, 13 réponses 503 sont suivies d'une réponse 200.
2. Les données sont toujours présentes après `down` puis `up`, mais `down -v` les supprime avec le volume.
3. Le mot de passe n'apparaît pas dans `docker history`, `docker image inspect`, les variables d'environnement ou les fichiers de l'image. Une recherche témoin retrouve bien du texte.
4. Après la suppression de la table, sa restauration depuis `preuves/sauvegarde.sql` permet de retrouver les trois lignes.

### Limites

Le mot de passe reste lisible dans le conteneur actif, car l'application en a besoin. Sous Docker Desktop pour Windows, le fichier monté apparaît avec des droits très larges (`rwxrwxrwx`). Le trafic entre l'application et la base n'est pas chiffré par TLS et aucune sauvegarde n'est planifiée. Enfin, les scénarios ont été vérifiés sous Windows seulement et ne sont pas automatisés.

## C3 — Cybersécurité et alertes

### Choix

- Je distingue les faits observés, les hypothèses et les mesures proposées. Le journal ne donne pas la cause des événements : les rejets de `partner-A` sont un signal à examiner, pas la preuve d'une attaque.
- La règle principale déclenche une alerte après au moins trois rejets `401 / bad_signature` provenant de la même source en 60 secondes. Elle est simple à expliquer, déterministe et testable.
- La journalisation utilise une liste blanche d'en-têtes. Un en-tête qui n'y figure pas n'est pas écrit dans le journal.
- J'ai implémenté la règle en Python et ajouté des tests. Le sujet demandait des exemples qui déclenchent ou non une alerte et une exécution reproductible ; les tests permettent de vérifier ces cas.

Un tableau avec du pseudo-code aurait été plus court, mais moins facile à vérifier. J'ai également écarté une détection par IA ou une méthode statistique : dans ce contexte, le résultat serait plus difficile à reproduire et à expliquer lors d'un incident.

### Résultats et limites

Le dossier [`c3/C3_dossier_cybersecurite.pdf`](c3/C3_dossier_cybersecurite.pdf) présente huit risques, les frontières de confiance, la règle, sept exemples et un runbook. `python -m c3` produit trois alertes : une rafale de signatures de `partner-A`, la livraison `d9` en quarantaine et le texte `e44` signalé. Les 16 tests passent.

La règle ne détectera pas une attaque répartie sur plusieurs sources ou plus lente que le seuil. Les heures du journal n'ont pas de date, donc le passage de minuit n'est pas géré. Enfin, les extraits disponibles ne permettent pas d'établir la cause de la panne de `d9` ni l'effet de `e44`.
