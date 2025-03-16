# SpotYnov API

## Description
SpotYnov API est un service d’extension des API Spotify permettant aux utilisateurs de créer un compte, se connecter, rejoindre des groupes et lier leur compte Spotify pour bénéficier de fonctionnalités avancées.

## Prérequis
Avant de commencer, assurez-vous d'avoir :
- Un **compte Spotify** actif.
- Une **application créée** dans votre espace développeur Spotify ([Dashboard Spotify](https://developer.spotify.com/dashboard/applications)).
- Node.js et Python installés sur votre machine.

## Installation

### 1. Cloner le projet
```bash
git clone https://github.com/Mael1to/SPOT_API-2-.git
cd spotynov-api
```

### 2. Installation des dépendances
#### Backend (Django)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend (React)
```bash
cd frontend
npm install
```

## Configuration de l'environnement

Avant de lancer le projet, assurez-vous de configurer correctement votre fichier **.env** pour la gestion des variables sensibles. Exemple :
```env
SPOTIFY_CLIENT_ID=f4382a97a0d24848aec0bfd4cef249a5
SPOTIFY_CLIENT_SECRET=deeca64e8e9a49ff8d20ae1ee74e1473
SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
SECRET_KEY=your_secret_key_here
DEBUG=True
```

## Lancement du projet

### 1. Démarrer le serveur Django (Backend)
Dans le dossier **backend**, exécutez :
```bash
python manage.py runserver
```
Le serveur est accessible à [http://127.0.0.1:8000](http://127.0.0.1:8000).

### 2. Démarrer l’application React (Frontend)
Dans le dossier **frontend**, exécutez :
```bash
npm start
```
L’application s’ouvrira dans le navigateur à [http://localhost:3000](http://localhost:3000).

## Fonctionnalités implémentées

### Partie 1 : Création et connexion utilisateur
- **FT-1** : Un utilisateur peut s’inscrire avec un pseudo unique et un mot de passe.
- **FT-2** : Un utilisateur peut se connecter et obtenir un token d’authentification (JWT).

#### Routes API
- **Inscription** : `POST /register/`
- **Connexion** : `POST /login/`
- **Rafraîchir le token** : `POST /token/refresh/`
- **Accès protégé** : `GET /protected/`

### Partie 2 : Gestion des Groupes
- **FT-3** : Un utilisateur peut créer un groupe et rejoindre un groupe existant.
- **FT-5** : Un utilisateur peut voir la liste des groupes existants et consulter les membres de son groupe.

#### Routes API
- **Créer un groupe** : `POST /groups/create/`
- **Rejoindre un groupe** : `POST /groups/join/`
- **Quitter un groupe** : `POST /groups/leave/`
- **Lister les groupes** : `GET /groups/`
- **Lister les membres d’un groupe** : `GET /groups/<group_name>/`

### Partie 3 : Liaison avec Spotify
- **FT-4** : Un utilisateur peut lier son compte Spotify.
- **FT-6** : Analyse des titres likés pour générer un profil musical.
- **FT-8** : Création d’une playlist des 10 morceaux favoris d’un utilisateur du groupe.

#### Routes API
- **Authentification Spotify** : `GET /spotify/auth/`
- **Callback Spotify** : `GET /spotify/callback/`

### Partie 4 : Sécurité et gestion des tokens
- **FT-10** : Sécurisation des routes via JWT.
- **FT-11** : Gestion des tokens d’authentification avec rafraîchissement automatique.

#### Routes API
- **Rafraîchir un token d’accès** : `POST /token/refresh/`

### Partie 5 : Conteneurisation et déploiement
- **FT-12** : Conteneurisation avec Docker.
- **FT-13** : Déploiement sur un serveur distant.

#### Commandes Docker
- **Construire l’image Docker** :
  ```bash
  docker build -t spotynov-api .
  ```
- **Lancer le conteneur** :
  ```bash
  docker run -p 8000:8000 spotynov-api
  ```

## Documentation API
L’API est documentée via Swagger et accessible à :
```
http://localhost:8000/swagger/
```

## Structure du projet
```
spotynov_api/
│── __pycache__/
│── asgi.py
│── settings.py
│── urls.py
│── wsgi.py
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
│── db.sqlite3
│── groups.json
│── manage.py

```

## Équipe
- **Compagny Maël** - parties 1, 2 et 3
- **Parduzi Erion** - parties 4 et 5
- ** ** - parties 6, 7 et 8
- ** ** - parties 

