import os
import requests
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserManager, GroupManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .utils import save_spotify_token
from rest_framework.decorators import api_view


SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"


import os
import requests
import json
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserManager, GroupManager
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .utils import save_spotify_token
from rest_framework.decorators import api_view

SPOTIFY_API_URL = "https://api.spotify.com/v1"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

def spotify_callback(request):
    """
    Gère le callback de l'authentification Spotify et stocke les tokens utilisateur.
    
    Cette fonction est appelée après que l'utilisateur a autorisé l'application via Spotify. 
    Elle récupère le code d'autorisation fourni par Spotify et échange ce code contre un 
    token d'accès et un token de rafraîchissement.
    
    **Méthode HTTP** : GET
    
    **Paramètres** (dans l'URL) :
    - `code` (str) : Code d'autorisation fourni par Spotify après authentification.
    - `state` (str) : Nom d'utilisateur de l'application associé à l'authentification.
    
    **Processus** :
    1. Vérifie que `code` et `state` sont bien présents.
    2. Effectue une requête à l'API Spotify pour échanger le `code` contre un `access_token` et un `refresh_token`.
    3. Stocke les tokens pour une utilisation future.
    
    **Réponses possibles** :
    - 200 : Succès, les tokens sont enregistrés.
    - 400 : Erreur si `code` ou `state` est manquant ou si l'échange de token échoue.
    """
    code = request.GET.get("code")
    username = request.GET.get("state")
    
    if not code:
        return JsonResponse({"error": "Code manquant"}, status=400)
    if not username:
        return JsonResponse({"error": "Nom d'utilisateur manquant"}, status=400)
    
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(SPOTIFY_TOKEN_URL, data=data, headers=headers)
    token_info = response.json()
    
    if "access_token" not in token_info:
        return JsonResponse({"error": "Échec de récupération du token", "details": token_info}, status=400)
    
    save_spotify_token(username, token_info["access_token"], token_info["refresh_token"])
    
    return JsonResponse({
        "message": "Spotify connecté avec succès !",
        "user": username,
        "tokens": {
            "access_token": token_info["access_token"],
            "refresh_token": token_info["refresh_token"]
        }
    })

class RegisterView(APIView):
    """
    Inscription d'un nouvel utilisateur.
    
    Cette classe permet à un utilisateur de s'inscrire en fournissant un nom d'utilisateur unique 
    et un mot de passe sécurisé. Le mot de passe sera stocké de manière sécurisée.
    
    **Méthode HTTP** : POST
    
    **Paramètres** (dans le corps de la requête) :
    - `username` (str) : Nom d'utilisateur unique.
    - `password` (str) : Mot de passe sécurisé.
    
    **Processus** :
    1. Vérifie que tous les champs sont fournis.
    2. Vérifie si l'utilisateur existe déjà.
    3. Crée un nouvel utilisateur et stocke ses informations.
    
    **Réponses possibles** :
    - 201 : Succès, l'utilisateur a été créé.
    - 400 : Erreur si des champs sont manquants ou si l'utilisateur existe déjà.
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = UserManager.create_user(username, password)
        return Response(result, status=status.HTTP_201_CREATED if "error" not in result else status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """
    Connexion d'un utilisateur existant.
    
    Cette classe permet à un utilisateur de se connecter en fournissant un nom d'utilisateur et 
    un mot de passe valide. Si l'authentification est réussie, un token JWT est généré.
    
    **Méthode HTTP** : POST
    
    **Paramètres** (dans le corps de la requête) :
    - `username` (str) : Nom d'utilisateur enregistré.
    - `password` (str) : Mot de passe associé au compte.
    
    **Processus** :
    1. Vérifie que tous les champs sont fournis.
    2. Authentifie l'utilisateur avec les identifiants fournis.
    3. Génère un token d'accès et un token de rafraîchissement.
    
    **Réponses possibles** :
    - 200 : Succès, retourne les tokens d'accès et de rafraîchissement.
    - 401 : Échec d'authentification si les identifiants sont incorrects.
    """
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = UserManager.authenticate_user(username, password)
        if user is None:
            return Response({"error": "Identifiants incorrects"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken()
        refresh["username"] = username

        return Response({
            "message": "Connexion réussie.",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)

class ProtectedView(APIView):
    """
    Accès à une route protégée nécessitant une authentification.
    
    Cette vue permet de vérifier si un utilisateur est correctement authentifié.
    Seuls les utilisateurs ayant un token valide peuvent accéder à cette ressource.
    
    **Méthode HTTP** : GET
    
    **Permissions** :
    - L'utilisateur doit être authentifié avec un token valide.
    
    **Réponses possibles** :
    - 200 : Succès, l'utilisateur est authentifié.
    - 403 : Accès refusé si l'utilisateur n'est pas authentifié.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Accès autorisé, tu es authentifié !"}, status=status.HTTP_200_OK)

class GroupListView(APIView):
    """
    Liste tous les groupes existants.
    
    Cette vue permet de récupérer la liste de tous les groupes créés dans l'application.
    
    **Méthode HTTP** : GET
    
    **Réponses possibles** :
    - 200 : Succès, retourne la liste des groupes.
    - 500 : Erreur serveur si la récupération des groupes échoue.
    """
    def get(self, request):
        groups = GroupManager.load_groups()
        if not isinstance(groups, dict):
            return Response({"error": "Problème de lecture des groupes"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(groups, status=status.HTTP_200_OK)

class GroupUsersView(APIView):
    """
    Liste les utilisateurs appartenant à un groupe donné.
    
    Cette vue permet de récupérer la liste des membres d'un groupe spécifique.
    
    **Méthode HTTP** : GET
    
    **Paramètres** :
    - `group_name` (str) : Nom du groupe dont on souhaite récupérer les membres.
    
    **Réponses possibles** :
    - 200 : Succès, retourne la liste des membres du groupe.
    - 404 : Erreur si le groupe n'existe pas.
    """
    def get(self, request, group_name):
        groups = GroupManager.load_groups()
        if group_name in groups:
            return Response(groups[group_name]["members"], status=status.HTTP_200_OK)
        return Response({"error": "Groupe introuvable"}, status=status.HTTP_404_NOT_FOUND)

class CreateGroupView(APIView):
    """
    Crée un nouveau groupe avec un administrateur.
    
    Cette vue permet de créer un groupe en lui attribuant un administrateur dès sa création.
    
    **Méthode HTTP** : POST
    
    **Paramètres** :
    - `group_name` (str) : Nom du groupe à créer.
    - `username` (str) : Nom d'utilisateur de l'administrateur du groupe.
    
    **Processus** :
    1. Vérifie que tous les champs requis sont fournis.
    2. Crée un nouveau groupe et assigne l'utilisateur comme administrateur.
    3. Retourne le groupe créé ou une erreur si la création échoue.
    
    **Réponses possibles** :
    - 201 : Succès, le groupe a été créé avec succès.
    - 400 : Erreur si des paramètres sont manquants ou invalides.
    - 500 : Erreur serveur en cas d'exception.
    """
    def post(self, request):
        try:
            data = request.data
            group_name = data.get("group_name")
            username = data.get("username")

            if not group_name or not username:
                return Response({"error": "Le nom du groupe et l'utilisateur sont requis."}, status=status.HTTP_400_BAD_REQUEST)

            result = GroupManager.create_group(group_name, username)

            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"Erreur serveur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class JoinGroupView(APIView):
    """
    Permet à un utilisateur de rejoindre un groupe existant.
    
    Cette vue permet à un utilisateur de rejoindre un groupe spécifié en fournissant son nom d'utilisateur.
    
    **Méthode HTTP** : POST
    
    **Paramètres** :
    - `group_name` (str) : Nom du groupe que l'utilisateur souhaite rejoindre.
    - `username` (str) : Nom d'utilisateur qui souhaite rejoindre le groupe.
    
    **Processus** :
    1. Vérifie que tous les champs requis sont fournis.
    2. Ajoute l'utilisateur au groupe spécifié.
    3. Retourne une confirmation ou une erreur si l'ajout échoue.
    
    **Réponses possibles** :
    - 200 : Succès, l'utilisateur a rejoint le groupe.
    - 400 : Erreur si des paramètres sont manquants ou invalides.
    - 500 : Erreur serveur en cas d'exception.
    """
    def post(self, request):
        try:
            data = request.data
            group_name = data.get("group_name")
            username = data.get("username")

            if not group_name or not username:
                return Response({"error": "Le nom du groupe et l'utilisateur sont requis."}, status=status.HTTP_400_BAD_REQUEST)

            result = GroupManager.join_group(group_name, username)

            if "error" in result:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Erreur serveur: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LeaveGroupView(APIView):
    """
    Permet à un utilisateur de quitter un groupe existant.
    
    Cette vue permet à un utilisateur de se retirer d'un groupe auquel il appartient.
    
    **Méthode HTTP** : POST
    
    **Paramètres** :
    - `username` (str) : Nom d'utilisateur souhaitant quitter le groupe.
    
    **Processus** :
    1. Vérifie que l'utilisateur est bien spécifié.
    2. Supprime l'utilisateur du groupe.
    3. Retourne une confirmation ou une erreur si l'opération échoue.
    
    **Réponses possibles** :
    - 200 : Succès, l'utilisateur a quitté le groupe.
    - 400 : Erreur si l'utilisateur n'est pas spécifié.
    - 500 : Erreur serveur en cas d'exception.
    """
    def post(self, request):
        username = request.data.get("username")

        if not username:
            return Response({"error": "Nom d'utilisateur requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = GroupManager.leave_group(username)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)

class UserPersonalityView(APIView):
    """
    Analyse les titres Spotify likés pour déterminer le style musical de l'utilisateur.
    
    Cette vue récupère les morceaux les plus écoutés de l'utilisateur sur Spotify afin 
    d'analyser sa préférence musicale en fonction de la popularité et de la durée moyenne des titres.
    
    **Méthode HTTP** : GET
    
    **Paramètres** :
    - `username` (str) : Nom d'utilisateur dont on souhaite analyser le style musical.
    
    **Processus** :
    1. Vérifie la présence d'un token Spotify valide.
    2. Récupère les titres les plus écoutés de l'utilisateur via l'API Spotify.
    3. Calcule la popularité et la durée moyenne des morceaux likés.
    
    **Réponses possibles** :
    - 200 : Succès, retourne l'analyse du style musical.
    - 401 : Erreur si le token Spotify est manquant.
    - 400 : Erreur si la récupération des titres likés échoue.
    """
    def get(self, request, username):
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Token Spotify manquant"}, status=status.HTTP_401_UNAUTHORIZED)

        headers = {"Authorization": token}
        response = requests.get(f"{SPOTIFY_API_URL}/me/top/tracks", headers=headers)

        if response.status_code != 200:
            return Response({"error": "Impossible de récupérer les titres likés"}, status=status.HTTP_400_BAD_REQUEST)

        tracks = response.json().get("items", [])
        if not tracks:
            return Response({"message": "Aucun titre liké"}, status=status.HTTP_200_OK)

        popularity = sum(track["popularity"] for track in tracks) / len(tracks)
        duration = sum(track["duration_ms"] for track in tracks) / len(tracks)

        return Response({"username": username, "popularity_average": popularity, "duration_average": duration}, status=status.HTTP_200_OK)

class SyncPlaybackView(APIView):
    """
    Synchronise la lecture de musique entre les membres d'un groupe.
    
    Cette vue permet à un administrateur de groupe de synchroniser sa lecture Spotify
    avec celle des autres membres du groupe.
    
    **Méthode HTTP** : POST
    
    **Paramètres** :
    - `group_name` (str) : Nom du groupe dont la lecture doit être synchronisée.
    - `Authorization` (str) : Token d'accès Spotify de l'utilisateur initiant la synchronisation.
    
    **Processus** :
    1. Vérifie la présence d'un token Spotify et d'un nom de groupe valide.
    2. Récupère la lecture en cours de l'administrateur via l'API Spotify.
    3. Si une musique est en cours de lecture, elle est synchronisée avec les membres du groupe.
    
    **Réponses possibles** :
    - 200 : Succès, la lecture est synchronisée.
    - 400 : Erreur si le token ou le nom du groupe est manquant.
    - 404 : Erreur si le groupe n'existe pas.
    - 400 : Erreur si aucune lecture en cours n'est détectée.
    """
    def post(self, request):
        token = request.headers.get("Authorization")
        group_name = request.data.get("group_name")

        if not token or not group_name:
            return Response({"error": "Token ou nom du groupe manquant"}, status=status.HTTP_400_BAD_REQUEST)

        headers = {"Authorization": token}
        playback = requests.get(f"{SPOTIFY_API_URL}/me/player", headers=headers)

        if playback.status_code != 200:
            return Response({"error": "Impossible de récupérer la lecture en cours"}, status=status.HTTP_400_BAD_REQUEST)

        track_info = playback.json()
        if not track_info.get("is_playing"):
            return Response({"message": "Aucune lecture en cours"}, status=status.HTTP_200_OK)

        track_uri = track_info["item"]["uri"]
        position_ms = track_info["progress_ms"]

        groups = GroupManager.load_groups()
        if group_name not in groups:
            return Response({"error": "Groupe introuvable"}, status=status.HTTP_404_NOT_FOUND)

        for member in groups[group_name]["members"]:
            if member != groups[group_name]["admin"]:
                requests.put(f"{SPOTIFY_API_URL}/me/player/play", json={"uris": [track_uri], "position_ms": position_ms}, headers=headers)

        return Response({"message": "Lecture synchronisée"}, status=status.HTTP_200_OK)

class SpotifyTokenView(APIView):
    """
    Récupère les tokens Spotify associés à un utilisateur.
    
    Cette vue permet de récupérer le token d'accès et le token de rafraîchissement 
    d'un utilisateur pour interagir avec l'API Spotify.
    
    **Méthode HTTP** : GET
    
    **Paramètres** :
    - `username` (str) : Nom d'utilisateur dont on souhaite récupérer les tokens Spotify.
    
    **Processus** :
    1. Vérifie si les tokens de l'utilisateur existent.
    2. Retourne les tokens trouvés ou une erreur si aucun token n'est disponible.
    
    **Réponses possibles** :
    - 200 : Succès, retourne les tokens Spotify.
    - 404 : Erreur si les tokens de l'utilisateur ne sont pas trouvés.
    """
    def get(self, request, username):
        tokens = UserManager.get_spotify_tokens(username)
        if tokens:
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"error": "Tokens non trouvés"}, status=status.HTTP_404_NOT_FOUND)

class SpotifyLoginView(APIView):
    """
    Génère une URL d'authentification Spotify pour l'utilisateur.
    
    Cette vue redirige l'utilisateur vers la page d'authentification Spotify afin de lier son compte
    avec l'application. Une fois l'authentification réussie, Spotify renverra un `code` permettant 
    d'obtenir un token d'accès.
    
    **Méthode HTTP** : GET
    
    **Paramètres** :
    - `username` (str) : Nom d'utilisateur demandant l'authentification.
    
    **Processus** :
    1. Génère une URL d'authentification Spotify avec les bons paramètres.
    2. Retourne cette URL pour que l'utilisateur puisse s'y connecter.
    
    **Réponses possibles** :
    - 200 : Succès, retourne l'URL d'authentification Spotify.
    """
    def get(self, request, username):
        auth_url = (
            f"https://accounts.spotify.com/authorize?"
            f"client_id={SPOTIFY_CLIENT_ID}"
            f"&response_type=code"
            f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
            f"&scope=user-read-playback-state user-modify-playback-state"
            f"&state={username}"
        )
        return Response({"auth_url": auth_url}, status=status.HTTP_200_OK)
