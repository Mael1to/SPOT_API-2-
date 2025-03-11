from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
import requests
import urllib.parse
from .models import UserManager, GroupManager

# Configuration Spotify
SPOTIFY_CLIENT_ID = settings.SPOTIFY_CLIENT_ID
SPOTIFY_CLIENT_SECRET = settings.SPOTIFY_CLIENT_SECRET
SPOTIFY_REDIRECT_URI = settings.SPOTIFY_REDIRECT_URI


# ---------------- AUTHENTIFICATION ----------------

class RegisterView(APIView):
    permission_classes = [AllowAny]  # Permet à tout le monde de s'inscrire

    def post(self, request):
        """Inscription d'un utilisateur"""
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = UserManager.create_user(username, password)
        return Response(result, status=status.HTTP_201_CREATED if "error" not in result else status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Permet à tout le monde de se connecter

    def post(self, request):
        """Connexion de l'utilisateur et génération du token JWT"""
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = UserManager.authenticate_user(username, password)
        if "error" in result:
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(username)  # Correctement généré
        return Response({
            "message": "Connexion réussie.",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)


class CustomTokenRefreshView(APIView):
    permission_classes = [AllowAny]  # Permet à tout le monde de rafraîchir son token

    def post(self, request):
        """Renouvellement du token JWT"""
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access_token = str(refresh.access_token)

            return Response({"access": new_access_token}, status=status.HTTP_200_OK)

        except Exception:
            return Response({"error": "Refresh token invalide"}, status=status.HTTP_401_UNAUTHORIZED)


# ---------------- GESTION DES GROUPES ----------------

class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Création d'un groupe"""
        group_name = request.data.get("group_name")
        if not group_name:
            return Response({"error": "Le nom du groupe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = GroupManager.create_group(group_name, request.user.username)
        return Response(result, status=status.HTTP_201_CREATED if "error" not in result else status.HTTP_400_BAD_REQUEST)


class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Rejoindre un groupe"""
        group_name = request.data.get("group_name")
        if not group_name:
            return Response({"error": "Le nom du groupe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = GroupManager.join_group(group_name, request.user.username)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)


class LeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Quitter un groupe"""
        result = GroupManager.leave_group(request.user.username)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)


class ListGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Liste des groupes"""
        result = GroupManager.load_groups()  # Correction ici
        return Response(result, status=status.HTTP_200_OK)


class ListGroupMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name):
        """Liste des membres d'un groupe"""
        result = GroupManager.list_group_members(group_name)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)


# ---------------- AUTHENTIFICATION SPOTIFY ----------------

class SpotifyAuthView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Génère l'URL d'authentification Spotify"""
        scope = "user-read-playback-state user-read-currently-playing user-library-read"
        auth_url = "https://accounts.spotify.com/authorize?"
        params = {
            "client_id": SPOTIFY_CLIENT_ID,
            "response_type": "code",
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "scope": scope,
        }
        return Response({"auth_url": auth_url + urllib.parse.urlencode(params)})


class SpotifyCallbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Récupération du token Spotify après redirection"""
        code = request.GET.get("code")
        if not code:
            return Response({"error": "Code manquant"}, status=400)

        token_url = "https://accounts.spotify.com/api/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": SPOTIFY_REDIRECT_URI,
            "client_id": SPOTIFY_CLIENT_ID,
            "client_secret": SPOTIFY_CLIENT_SECRET,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        response = requests.post(token_url, data=data, headers=headers)
        token_info = response.json()

        if "access_token" not in token_info:
            return Response({"error": "Échec de l'authentification Spotify"}, status=400)

        users = UserManager.load_users()
        users[request.user.username]["spotify_token"] = token_info
        UserManager.save_users(users)

        return Response({"message": "Compte Spotify lié avec succès", "spotify_token": token_info})

class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Accès autorisé, tu es authentifié !"}, status=status.HTTP_200_OK)

