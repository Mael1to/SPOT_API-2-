import json
import hashlib
import os
import random

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

    @staticmethod
    def authenticate_user(username, password):
        """Vérifie si l'utilisateur existe et si le mot de passe est correct."""
        users = UserManager.load_users()

        if username not in users:
            return {"error": "Nom d'utilisateur ou mot de passe incorrect."}

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if users[username]["password"] != hashed_password:
            return {"error": "Nom d'utilisateur ou mot de passe incorrect."}

        return {"message": "Connexion réussie."}


GROUPS_FILE = "groups.json"

class GroupManager:
    @staticmethod
    def load_groups():
        """Charge les groupes depuis le fichier JSON."""
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
        """Sauvegarde les groupes dans le fichier JSON."""
        with open(GROUPS_FILE, "w") as f:
            json.dump(groups, f, indent=4)

    @staticmethod
    def get_user_group(username):
        """Trouve le groupe auquel appartient un utilisateur."""
        groups = GroupManager.load_groups()
        for group, data in groups.items():
            if username in data["members"]:
                return group
        return None

    @staticmethod
    def create_group(group_name, creator):
        """Crée un groupe et désigne le créateur comme administrateur après l'avoir fait quitter son ancien groupe."""
        groups = GroupManager.load_groups()

        user_group = GroupManager.get_user_group(creator)
        leave_message = None 

        if user_group:
            leave_result = GroupManager.leave_group(creator)
            if "error" not in leave_result:
                leave_message = leave_result["message"]
                groups = GroupManager.load_groups()  

        if group_name in groups:
            return {"error": "Ce groupe existe déjà."}
     
        groups[group_name] = {
            "members": [creator],
            "admin": creator
        }
        GroupManager.save_groups(groups)

        response = {
            "message": f"Groupe '{group_name}' créé avec succès.",
            "admin": creator
        }
        if leave_message:
            response["previous_group_left"] = leave_message  

        return response

    @staticmethod
    def leave_group(username):
        """Permet à un utilisateur de quitter son groupe actuel."""
        groups = GroupManager.load_groups()
        user_group = GroupManager.get_user_group(username)

        if not user_group:
            return {"error": "L'utilisateur n'appartient à aucun groupe."}

        groups[user_group]["members"].remove(username)

        if not groups[user_group]["members"]:
            del groups[user_group] 
            GroupManager.save_groups(groups)
            return {
                "message": f"{username} a quitté le groupe '{user_group}'.",
                "info": f"Le groupe '{user_group}' a été supprimé car il n'avait plus de membres."
            }

        if "admin" in groups[user_group] and groups[user_group]["admin"] == username:
            if groups[user_group]["members"]:
                new_admin = random.choice(groups[user_group]["members"])
                groups[user_group]["admin"] = new_admin
            else:
                del groups[user_group]

        GroupManager.save_groups(groups)

        return {"message": f"{username} a quitté le groupe '{user_group}'."}

    @staticmethod
    def join_group(group_name, username):
        """Ajoute un utilisateur à un groupe existant, ou le crée s'il n'existe pas."""
        groups = GroupManager.load_groups()

        user_group = GroupManager.get_user_group(username)
        leave_message = None  

        if user_group:
            leave_result = GroupManager.leave_group(username)  
            if "error" not in leave_result:
                leave_message = leave_result["message"]
                groups = GroupManager.load_groups()  

        if group_name not in groups:
            create_result = GroupManager.create_group(group_name, username)
            if leave_message:
                create_result["previous_group_left"] = leave_message
            return create_result

        groups[group_name]["members"].append(username)
        GroupManager.save_groups(groups)

        response = {"message": f"{username} a rejoint le groupe '{group_name}'."}
        if leave_message:
            response["previous_group_left"] = leave_message

        return response

    @staticmethod
    def list_groups():
        """Retourne la liste de tous les groupes et le nombre de membres."""
        groups = GroupManager.load_groups()
        return [{"name": name, "nombre_utilisateurs": len(data["members"])} for name, data in groups.items()]
