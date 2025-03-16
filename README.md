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

### Partie 2 : Gestion des Groupes
- **FT-3** : Un utilisateur peut rejoindre un groupe. Si le groupe n’existe pas, il est créé et l’utilisateur devient administrateur.
- **FT-5** : Un utilisateur peut voir la liste des groupes existants et consulter les membres de son groupe.

### Partie 3 : Liaison avec Spotify
- **FT-4** : Un utilisateur peut lier son compte Spotify pour permettre au service d’accéder aux API Spotify.
- **FT-6** : Analyse des titres likés pour générer un profil musical.
- **FT-8** : Création d’une playlist des 10 morceaux favoris d’un utilisateur du groupe.

## Documentation API
L’API est documentée via Swagger et accessible à :
```
http://localhost:8000/swagger/
```

## Structure du projet
```
spotynov-api/
│── backend/         # API Django
│   ├── api/         # Logique métier et endpoints
│   ├── users/       # Gestion des utilisateurs
│   ├── groups/      # Gestion des groupes
│   ├── spotify/     # Liaison avec Spotify
│   └── requirements.txt
│── frontend/        # Application React
│   ├── src/
│   ├── public/
│   ├── package.json
│── README.md        # Ce fichier
```

## Équipe
- **Compagny Maël** - parties 1, 2 et 3
- **Parduzi Erion** - parties 4 et 5
- ** ** - parties 6, 7 et 8
- ** ** - parties 

