# Melosite

Une application web pour la gestion de vélos.

## Prérequis

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation avec Docker

1. Clonez ce dépôt :
   ```bash
   git clone <repository-url>
   cd melosite
   ```

2. Construisez et démarrez les conteneurs avec Docker Compose :
   ```bash
   docker-compose up -d --build
   ```

3. L'application sera accessible à l'adresse https://localhost:5001

## Arrêt des conteneurs

Pour arrêter les conteneurs sans les supprimer :
```bash
docker-compose stop
```

Pour arrêter et supprimer les conteneurs (les données de la base de données seront conservées) :
```bash
docker-compose down
```

Pour arrêter et supprimer les conteneurs ainsi que les volumes (toutes les données seront perdues) :
```bash
docker-compose down -v
```

## Développement

Pour le développement, les fichiers locaux sont montés dans le conteneur, ce qui signifie que les modifications apportées aux fichiers locaux seront reflétées dans l'application en cours d'exécution.

## Performance

Des optimisations ont été mises en place pour améliorer les performances de l'application, notamment :

- Indexation de la table des vélos pour accélérer les requêtes fréquentes
- Optimisation des requêtes pour réduire le nombre d'appels à la base de données
- Mise à jour des statistiques pour le planificateur de requêtes PostgreSQL

Pour plus de détails sur les optimisations, consultez le fichier [OPTIMIZATION.md](OPTIMIZATION.md).

## Roadmap

### Road to V0:
- Ajouter la page de gestion admin:
  - Suppression d'un vélo

### Road to V1:
- Ajouter un pop-up lorsqu'on sort le vélo du stock (aka de enstock à vendu/donné/etc...)
- Ajouter gestion d'erreur avec enregistrement de log
