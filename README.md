# TP 2 MongoDB

## Base de données MongoDB avec Docker

Exécuter la commande suivante pour lancer le conteneur definit dans le fichier `docker-compose.yml`
```bash
docker-compose up -d
```

## Installation

1. Créer un environnement virtuel
```bash
python3 -m venv .venv
```

2. Activer l'environnement virtuel
```bash
source .venv/bin/activate
```

3. Installer les dépendances
```bash
pip install -r requirements.txt
```

## Peuplement de la base de données

Lancer le script de peuplement
```bash
python seed.py
```
