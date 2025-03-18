import json
import hashlib
import os
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")
GROUPS_FILE = "groups.json"

class UserManager:
    """
    Gestion des utilisateurs via un fichier JSON.
    
    Cette classe permet de gérer les utilisateurs en les stockant dans un fichier JSON.
    Elle offre des fonctionnalités pour la création, l'authentification et la récupération 
    des tokens Spotify des utilisateurs.
    
    **Méthodes** :
    - `load_users()`: Charge les utilisateurs depuis `users.json`.
    - `save_users(users)`: Sauvegarde les utilisateurs dans `users.json`.
    - `create_user(username, password)`: Crée un nouvel utilisateur avec un mot de passe hashé.
    - `authenticate_user(username, password)`: Vérifie l'identité d'un utilisateur.
    - `get_spotify_tokens(username)`: Récupère les tokens Spotify d'un utilisateur.
    """
    @staticmethod
    def load_users():
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_users(users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def create_user(username, password):
        """
        Crée un utilisateur avec un mot de passe hashé.
        
        **Paramètres** :
        - `username` (str) : Nom d'utilisateur à créer.
        - `password` (str) : Mot de passe en clair, qui sera hashé avant stockage.
        
        **Processus** :
        1. Charge la liste des utilisateurs existants.
        2. Vérifie si l'utilisateur existe déjà.
        3. Hash le mot de passe et stocke l'utilisateur.
        4. Sauvegarde la nouvelle liste des utilisateurs.
        
        **Retour** :
        - Message de succès si l'utilisateur est créé.
        - Message d'erreur si l'utilisateur existe déjà.
        """
        users = UserManager.load_users()
        if username in users:
            return {"error": "Utilisateur déjà existant."}

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users[username] = {"password": hashed_password}
        UserManager.save_users(users)
        return {"message": "Utilisateur créé avec succès."}

    @staticmethod
    def authenticate_user(username, password):
        """
        Vérifie l'authentification d'un utilisateur.
        
        **Paramètres** :
        - `username` (str) : Nom d'utilisateur à vérifier.
        - `password` (str) : Mot de passe en clair à comparer avec le hash stocké.
        
        **Processus** :
        1. Charge la liste des utilisateurs.
        2. Vérifie si l'utilisateur existe.
        3. Hash le mot de passe fourni et compare avec celui enregistré.
        4. Retourne l'utilisateur si l'authentification est réussie.
        
        **Retour** :
        - Dictionnaire contenant `username` si l'authentification réussit.
        - `None` si l'authentification échoue.
        """
        users = UserManager.load_users()
        if username not in users:
            return None  

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if users[username]["password"] != hashed_password:
            return None  

        return {"username": username}

    @staticmethod
    def get_spotify_tokens(username):
        """
        Récupère les tokens Spotify d'un utilisateur.
        
        **Paramètres** :
        - `username` (str) : Nom d'utilisateur dont on veut récupérer les tokens Spotify.
        
        **Processus** :
        1. Charge la liste des utilisateurs.
        2. Vérifie si l'utilisateur possède des tokens Spotify.
        3. Retourne les tokens ou `None` si absents.
        
        **Retour** :
        - Un dictionnaire contenant `access_token` et `refresh_token` si disponibles.
        - `None` si les tokens n'existent pas.
        """
        users = UserManager.load_users()
        if username in users and "spotify_access_token" in users[username]:
            return {
                "access_token": users[username]["spotify_access_token"],
                "refresh_token": users[username]["spotify_refresh_token"]
            }
        return None

class GroupManager:
    """
    Gestion des groupes via un fichier JSON.
    
    Cette classe permet de créer, gérer et supprimer des groupes d'utilisateurs.
    Les groupes sont stockés dans un fichier JSON.
    
    **Méthodes** :
    - `load_groups()`: Charge les groupes depuis `groups.json`.
    - `save_groups(groups)`: Sauvegarde les groupes dans `groups.json`.
    - `get_user_group(username)`: Trouve le groupe auquel appartient un utilisateur.
    - `leave_group(username)`: Permet à un utilisateur de quitter un groupe.
    - `create_group(group_name, creator)`: Crée un groupe avec un administrateur.
    - `join_group(group_name, username)`: Ajoute un utilisateur à un groupe existant.
    """
    @staticmethod
    def load_groups():
        """
        Charge les groupes depuis le fichier `groups.json`.
        
        **Processus** :
        1. Vérifie si `groups.json` existe, sinon le crée.
        2. Lit et charge le contenu JSON du fichier.
        3. Retourne les groupes sous forme de dictionnaire.
        
        **Retour** :
        - Un dictionnaire contenant les groupes et leurs membres.
        - Un dictionnaire vide si le fichier est inexistant ou corrompu.
        """
        if not os.path.exists(GROUPS_FILE):
            with open(GROUPS_FILE, "w") as f:
                json.dump({}, f)

        try:
            with open(GROUPS_FILE, "r") as f:
                data = f.read().strip()
                return json.loads(data) if data else {}
        except json.JSONDecodeError:
            return {}

    @staticmethod
    def save_groups(groups):
        """
        Sauvegarde les groupes dans `groups.json`.
        
        **Processus** :
        1. Ouvre `groups.json` en mode écriture.
        2. Écrit les groupes avec une indentation pour lisibilité.
        
        **Erreurs possibles** :
        - Affiche un message si l'écriture échoue.
        """
        with open(GROUPS_FILE, "w") as f:
            json.dump(groups, f, indent=4)

    @staticmethod
    def get_user_group(username):
        """
        Trouve le groupe auquel appartient un utilisateur.
        
        **Paramètres** :
        - `username` (str) : Nom d'utilisateur recherché.
        
        **Retour** :
        - Le nom du groupe si l'utilisateur en fait partie.
        - `None` si l'utilisateur n'appartient à aucun groupe.
        """
        groups = GroupManager.load_groups()
        for group, data in groups.items():
            if "members" in data and username in data["members"]:
                return group
        return None

    @staticmethod
    def leave_group(username):
        """
        Permet à un utilisateur de quitter son groupe actuel.
        
        **Paramètres** :
        - `username` (str) : Nom d'utilisateur quittant le groupe.
        
        **Retour** :
        - Message confirmant le départ de l'utilisateur.
        - Message d'erreur si l'utilisateur n'appartient à aucun groupe.
        """
        groups = GroupManager.load_groups()
        user_group = GroupManager.get_user_group(username)

        if not user_group:
            return {"error": "L'utilisateur n'appartient à aucun groupe."}

        groups[user_group]["members"].remove(username)

        if not groups[user_group]["members"]:
            del groups[user_group]
        elif "admin" in groups[user_group] and groups[user_group]["admin"] == username:
            groups[user_group]["admin"] = random.choice(groups[user_group]["members"])

        GroupManager.save_groups(groups)

        return {"message": f"{username} a quitté le groupe '{user_group}'."}

    @staticmethod
    def create_group(group_name, creator):
        """
        Crée un groupe avec un administrateur.
        
        **Paramètres** :
        - `group_name` (str) : Nom du groupe à créer.
        - `creator` (str) : Nom d'utilisateur de l'administrateur du groupe.
        
        **Retour** :
        - Message confirmant la création du groupe.
        - Message d'erreur si le groupe existe déjà.
        """
        groups = GroupManager.load_groups()

        if group_name in groups:
            return {"error": "Ce groupe existe déjà."}

        groups[group_name] = {
            "members": [creator],
            "admin": creator
        }
        GroupManager.save_groups(groups)

        return {"message": f"Groupe '{group_name}' créé avec succès.", "admin": creator}

    @staticmethod
    def join_group(group_name, username):
        """
        Ajoute un utilisateur à un groupe existant.
        
        **Paramètres** :
        - `group_name` (str) : Nom du groupe à rejoindre.
        - `username` (str) : Nom d'utilisateur à ajouter au groupe.
        
        **Retour** :
        - Message confirmant l'ajout de l'utilisateur.
        - Message d'erreur si le groupe n'existe pas ou si l'utilisateur est déjà membre.
        """
        groups = GroupManager.load_groups()

        if group_name not in groups:
            return {"error": "Ce groupe n'existe pas."}

        if username in groups[group_name]["members"]:
            return {"error": f"L'utilisateur {username} est déjà dans le groupe."}

        groups[group_name]["members"].append(username)
        GroupManager.save_groups(groups)

        return {"message": f"{username} a rejoint le groupe '{group_name}'."}