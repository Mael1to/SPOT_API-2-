from django.db import models

import json
import hashlib
import os

USERS_FILE = "users.json"

class UserManager:
    @staticmethod
    def load_users():
        """Charge les utilisateurs depuis le fichier JSON."""
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_users(users):
        """Sauvegarde les utilisateurs dans le fichier JSON."""
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)

    @staticmethod
    def create_user(username, password):
        """Ajoute un nouvel utilisateur si le pseudo est unique."""
        users = UserManager.load_users()
        if username in users:
            return {"error": "Le nom d'utilisateur est déjà pris."}

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        users[username] = {"password": hashed_password}
        UserManager.save_users(users)

        return {"message": "Utilisateur créé avec succès."}

