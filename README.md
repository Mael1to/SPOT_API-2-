# SpotYnov API

## Description
SpotYnov API est un service d’extension des API Spotify permettant aux utilisateurs de créer un compte, se connecter, rejoindre des groupes et lier leur compte Spotify pour bénéficier de fonctionnalités avancées, notamment la consultation de leur profil musical et la gestion de playlists collaboratives.

## Prérequis
Avant de commencer, assurez-vous d'avoir :
- Un **compte Spotify** actif.
- Une **application créée** dans votre espace développeur Spotify ([Dashboard Spotify](https://developer.spotify.com/dashboard/applications)).
- **Python** installés sur votre machine.

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Mael1to/SPOT_API-2-.git
cd spotynov-api
```

### 2. Créer un environnement virtuel (optionnel mais recommandé)
```bash
python -m venv venv
source venv/bin/activate  # Sur MacOS/Linux
venv\Scripts\activate    # Sur Windows
```

### 3. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 4. Installer Swagger UI pour la documentation de l'API
```bash
pip install drf-yasg
```

## Lancement du projet

### 1. Démarrer le serveur Django
```bash
python manage.py runserver
```
Le serveur est accessible à [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Fonctionnalités implémentées

### 🟢 Partie 1 : Gestion des utilisateurs
- **FT-1** : Création d'un compte utilisateur avec pseudo et mot de passe.
- **FT-2** : Connexion et authentification avec un token JWT.

#### Routes API
- **Inscription** : `POST /api/register/`
- **Connexion** : `POST /api/login/`
- **Accès protégé** : `GET /api/protected/`
- **Obtenir un token** : `POST /api/token/`
- **Rafraîchir un token** : `POST /api/token/refresh/`

### 🟢 Partie 2 : Gestion des groupes
- **FT-3** : Création et adhésion à un groupe.
- **FT-5** : Consultation de la liste des groupes et de leurs membres.

#### Routes API
- **Lister les groupes** : `GET /api/groups/`
- **Créer un groupe** : `POST /api/groups/create/`
- **Rejoindre un groupe** : `POST /api/groups/join/`
- **Quitter un groupe** : `POST /api/groups/leave/`
- **Lister les membres d’un groupe** : `GET /api/groups/<group_name>/users/`
- **Synchronisation de la lecture** : `POST /api/groups/sync/`

### 🟢 Partie 3 : Intégration Spotify
- **FT-4** : Liaison du compte Spotify.
- **FT-6** : Analyse des titres likés pour générer un profil musical.
- **FT-8** : Création d’une playlist basée sur les morceaux favoris d’un utilisateur.

#### Routes API
- **Obtenir la personnalité utilisateur** : `GET /api/users/<username>/personality/`
- **Obtenir les tokens Spotify** : `GET /api/spotify/tokens/<username>/`
- **Authentification Spotify** : `GET /api/spotify/login/<username>/`
- **Callback Spotify** : `GET /api/spotify/callback/`

## Documentation API
L’API est documentée via Swagger et accessible à :
```
http://localhost:8000/swagger/
```

## Structure du projet
```
SPOT_API/
│── spotynov_api/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│   ├── wsgi.py
│── users/
│   ├── __pycache__/
│   ├── migrations/
│   │   ├── __init__.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── authentication.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── utils.py
│   ├── users.json
│── .env
│── db.sqlite3
│── groups.json
│── manage.py
│── venv/
│── README.md
```

## Équipe
- **Compagny Maël** - Gestion des utilisateurs et groupes
- **Parduzi Erion-Philibert Bastien** - Authentification et sécurité
- **El Mokretar Ahlem Oumnia-Philibert Bastien** - Liaison Spotify et gestion musicale
- **Philibert Bastien** - Documentation
