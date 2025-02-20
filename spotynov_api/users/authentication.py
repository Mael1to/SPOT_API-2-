from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import UserManager

class CustomUser:
    def __init__(self, user_id, username):
        self.id = user_id
        self.username = username
        self.is_authenticated = True  

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Récupère l'utilisateur à partir du token JWT sans base de données.
        """
        user_id = validated_token.get("user_id", None)
        username = validated_token.get("username", None)

        if not username:
            raise AuthenticationFailed({"detail": "User not found", "code": "user_not_found"})

        users = UserManager.load_users()

        if username not in users:
            raise AuthenticationFailed({"detail": "User not found", "code": "user_not_found"})

        return CustomUser(user_id, username)
