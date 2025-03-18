import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USERS_FILE = os.path.join(BASE_DIR, "users.json")

def load_users():
    """
    Charge les utilisateurs depuis le fichier `users.json`, en vérifiant qu'il est lisible.
    
    Cette fonction s'assure que le fichier existe et contient des données JSON valides.
    Si le fichier est corrompu ou inaccessible, une alerte est affichée et un dictionnaire vide est retourné.
    
    **Processus** :
    1. Vérifie l'existence du fichier `users.json`.
    2. Ouvre le fichier et charge son contenu en JSON.
    3. Gère les erreurs liées à la lecture ou au format du fichier.
    
    **Réponses possibles** :
    - Retourne un dictionnaire contenant les utilisateurs si le fichier est valide.
    - Retourne un dictionnaire vide en cas d'erreur.
    """
    if not os.path.exists(USERS_FILE):
        return {}

    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, IOError):
        print("Erreur : Le fichier users.json est corrompu ou inaccessible.")
        return {}

def save_users(users):
    """
    Sauvegarde les utilisateurs dans le fichier `users.json` de manière sécurisée.
    
    Cette fonction écrit les données utilisateur dans le fichier JSON avec un format lisible
    en ajoutant une indentation.
    
    **Processus** :
    1. Ouvre le fichier `users.json` en mode écriture.
    2. Écrit le dictionnaire des utilisateurs en JSON formaté.
    3. Gère les erreurs d'écriture éventuelles.
    
    **Erreurs possibles** :
    - Affiche un message d'erreur si l'écriture dans le fichier échoue.
    """
    try:
        with open(USERS_FILE, "w") as file:
            json.dump(users, file, indent=4)
    except IOError:
        print("Erreur lors de l'écriture dans users.json")

def save_spotify_token(username, access_token, refresh_token):
    """
    Sauvegarde les tokens Spotify d'un utilisateur dans le fichier `users.json`.
    
    Cette fonction met à jour ou ajoute les tokens Spotify d'un utilisateur donné 
    dans le fichier JSON.
    
    **Processus** :
    1. Vérifie que `username` est valide.
    2. Vérifie et crée le fichier `users.json` s'il n'existe pas.
    3. Charge les utilisateurs existants ou initialise une nouvelle structure JSON.
    4. Ajoute ou met à jour les tokens Spotify de l'utilisateur.
    5. Sauvegarde les nouvelles données dans `users.json`.
    
    **Erreurs possibles** :
    - Affiche un message d'erreur si `username` est vide.
    - Affiche un message si le fichier est inaccessible.
    """
    print(f"DEBUG: save_spotify_token appelé avec username={username}")
    
    if not username:
        print("⚠️ ERREUR: Username vide !")
        return  # Stopper l'exécution si `username` est vide

    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as file:
            json.dump({}, file)

    try:
        with open(USERS_FILE, "r+") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}

            if username not in users:
                users[username] = {}

            users[username]["spotify_access_token"] = access_token
            users[username]["spotify_refresh_token"] = refresh_token

            file.seek(0)
            json.dump(users, file, indent=4)
            file.truncate()

    except IOError:
        print("Erreur d'accès au fichier users.json")
