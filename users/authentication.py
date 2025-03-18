from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserManager

class CustomUser:
    """
    Représente un utilisateur sans base de données.
    
    Cette classe est utilisée pour gérer des utilisateurs en session sans persistance en base de données.
    
    **Attributs** :
    - `username` (str) : Nom d'utilisateur associé à l'objet utilisateur.
    - `is_authenticated` (bool) : Toujours `True`, car cet utilisateur est considéré comme authentifié.
    
    **Méthodes** :
    - `__init__(username)`: Initialise un utilisateur avec un nom d'utilisateur.
    """
    def __init__(self, username):
        self.username = username
        self.is_authenticated = True  

class CustomJWTAuthentication(JWTAuthentication):
    """
    Authentification JWT personnalisée avec `users.json`.
    
    Cette classe surcharge l'authentification JWT pour récupérer les utilisateurs depuis un fichier JSON 
    au lieu d'une base de données.
    
    **Méthodes** :
    - `get_user(validated_token)`: Vérifie et retourne l'utilisateur authentifié basé sur le token JWT.
    
    **Processus** :
    1. Extrait le nom d'utilisateur du token JWT validé.
    2. Vérifie si l'utilisateur existe dans le système d'authentification.
    3. Retourne une instance de `CustomUser` si l'utilisateur est valide.
    
    **Exceptions** :
    - `AuthenticationFailed` : Si l'utilisateur n'existe pas ou est invalide.
    """
    def get_user(self, validated_token):
        username = validated_token.get("username", None)

        if not username:
            raise AuthenticationFailed({"detail": "Utilisateur non trouvé", "code": "user_not_found"})

        user = UserManager.authenticate_user(username, None)

        if user is None:
            raise AuthenticationFailed({"detail": "Utilisateur non trouvé", "code": "user_not_found"})

        return CustomUser(username)
