# Sources et usages de l'IA

## 1. Outil utilisé

Pour réaliser ce projet de rattrapage, j'ai utilisé **Claude (Anthropic)**, accessible sur [claude.ai](https://claude.ai).

Je m'en suis principalement servi comme d'un assistant pour m'aider à comprendre les consignes, avancer dans le développement des différents modules et améliorer les documents que je devais rendre.

## 2. Comment j'ai utilisé l'IA

J'ai travaillé progressivement sur les trois parties du projet : C3, C4 et I2. Mon objectif était de comprendre ce que je faisais, de réussir à exécuter le projet sur mon ordinateur et de vérifier que les résultats correspondaient aux consignes.

Au début, j'ai demandé à Claude de m'expliquer le sujet et de me guider étape par étape. Je lui ai ensuite posé des questions sur les notions que je ne comprenais pas, notamment les journaux d'événements, les risques de sécurité, les webhooks, les injections de prompt, Docker et la normalisation des données.

Claude m'a également aidé à développer les différents modules en proposant du code et en m'expliquant le rôle des fichiers. De mon côté, j'ai suivi les étapes, exécuté les commandes, testé les fonctionnalités et vérifié les résultats obtenus. J'ai aussi dû adapter certaines instructions à mon environnement Windows et PowerShell.

Enfin, j'ai utilisé Claude pour améliorer la présentation des livrables, corriger certaines formulations et organiser les fichiers de documentation.

## 3. Utilisation de Claude selon les parties du projet

### C3 – Analyse et cybersécurité

Pour C3, j'ai commencé par étudier le sujet et répondre aux questions concernant le journal d'événements et la configuration présentée.

J'ai ensuite utilisé Claude pour vérifier mon raisonnement, corriger certaines erreurs et mieux expliquer les risques identifiés. Par exemple, j'ai travaillé sur l'interprétation des rejets de `partner-A`, l'échec de livraison de `d9`, les risques liés à l'exposition de la base de données et les droits administrateur.

À partir de mes réponses et des corrections apportées, Claude m'a aidé à structurer et à mettre en forme le dossier d'analyse au format PDF.

J'ai également vérifié si des tests Python étaient obligatoires pour cette partie afin de justifier les choix retenus dans `JUSTIFICATIONS.md`.

### C4 – Sécurité et Docker

Pour C4, j'ai utilisé Claude pour comprendre les consignes et mettre en place les fichiers nécessaires au fonctionnement du projet.

J'ai ensuite effectué les manipulations sur mon ordinateur sous Windows, notamment la création des fichiers de test, l'exécution des commandes Docker et la vérification des scénarios.

J'ai exécuté les quatre scénarios prévus, dont celui concernant l'attente de la disponibilité de la base de données. J'ai dû relancer ce dernier après un premier essai trop rapide.

J'ai également vérifié que les fichiers contenant des secrets de test n'étaient pas suivis par Git. Pour cela, j'ai notamment utilisé `git check-ignore`.

Pendant cette partie, j'ai aussi adapté la documentation à mon environnement PowerShell et organisé les preuves d'exécution dans `c4/preuves/scenarios.md`.

### I2 – Traitement des données

Pour I2, Claude m'a aidé à construire le module et à comprendre le traitement des données, les rejets et la détection des doublons.

Une fois le module mis en place, je l'ai exécuté avec `python -m i2`. J'ai vérifié que le tableau de bord s'ouvrait dans le navigateur, puis j'ai consulté les fichiers `rejets.json` et `doublons.json` pour comprendre les résultats produits.

J'ai également exécuté les tests afin de vérifier le fonctionnement du module.

## 4. Travail réalisé et vérifications personnelles

Même si Claude m'a aidé pendant le développement, j'ai effectué moi-même les manipulations dans mon environnement de travail. J'ai notamment :

- configuré Git et créé le dépôt public GitHub `Matrice_Rattrapage` ;
- corrigé l'adresse du dépôt distant après une erreur de configuration ;
- exécuté les commandes Python, PowerShell et Docker ;
- testé les fonctionnalités des trois modules ;
- vérifié les résultats et les fichiers générés ;
- contrôlé que les secrets de test n'étaient pas versionnés ;
- organisé les preuves et la documentation ;
- effectué les commits module par module et envoyé les modifications sur GitHub.

J'ai aussi choisi de produire le dossier d'analyse C3 au format PDF.

Ces manipulations m'ont permis de suivre le fonctionnement du projet, de comprendre les erreurs rencontrées et de vérifier que les livrables fonctionnaient dans mon environnement.

## 5. Vérifications effectuées

Voici les principales vérifications réalisées à la fin du travail :

| Partie | Vérifications |
|---|---|
| C3 | Exécution avec `python -m c3` et 16 tests réussis. |
| C4 | Exécution des quatre scénarios sous Windows avec Docker, puis conservation des résultats dans `c4/preuves/scenarios.md`. |
| I2 | Exécution avec `python -m i2`, ouverture du tableau de bord, 13 tests réussis et vérification des fichiers de rejets et de doublons. |
| Git | Vérification des fichiers ignorés et contrôle des fichiers suivis dans le dépôt. |

La commande `git ls-files` ne faisait apparaître que `c4/secrets/db_password.txt.example` pour le fichier d'exemple concerné. Aucun secret réel n'a été ajouté au dépôt.

## 6. Requêtes utilisées

Voici quelques exemples de demandes que j'ai formulées pendant le travail :

- « Voici le sujet du rattrapage » : pour commencer par comprendre les attentes du projet.
- « Bon, recommençons depuis le début avec C3, tu vas me guider dans ce que je dois faire tout en m'expliquant » : pour avancer progressivement et comprendre les étapes.
- « Fais-moi un PDF à l'aide de mes réponses en les améliorant de manière à remplir les conditions de C3 » : pour améliorer la présentation et la précision de mon analyse.
- « Passons au C4 » : pour continuer le travail sur la partie suivante.
- « Continuons les exercices, passons à I2 » : pour poursuivre le développement du dernier module.

Ces échanges illustrent mon utilisation de Claude pour obtenir des explications, progresser dans le développement et améliorer les livrables.

## 7. Autres sources

La principale source utilisée pour définir le travail à réaliser est l'énoncé du rattrapage fourni avec le sujet.

**Autres outils d'IA utilisés :** [à compléter selon les outils réellement utilisés].

**Documentation externe consultée :** [à compléter si des sites, cours ou documentations ont été utilisés].

## 8. Compréhension personnelle du projet

Mon objectif n'était pas seulement d'obtenir des fichiers qui fonctionnent, mais aussi de comprendre les étapes nécessaires pour les mettre en place et les vérifier.

L'utilisation de Claude m'a aidé à progresser lorsque je rencontrais une difficulté, mais j'ai dû appliquer les instructions, exécuter les commandes, observer les résultats et corriger les problèmes rencontrés dans mon environnement.

Je dois pouvoir expliquer le rôle des principaux fichiers, les choix effectués et les tests réalisés. Cette compréhension est importante pour pouvoir présenter et défendre mon travail.
