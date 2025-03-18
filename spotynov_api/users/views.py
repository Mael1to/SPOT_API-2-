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
import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Group 

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



class SyncPlaybackView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        user = request.user 
        spotify_token = user.spotify_token
        if not spotify_token:
            return JsonResponse({"error": "Spotify account not linked"}, status=403)


        try:
            group = Group.objects.get(admin=user)
        except Group.DoesNotExist:
            return JsonResponse({"error": "You are not an administrator of any group"}, status=403)

        playback_url = "https://api.spotify.com/v1/me/player/currently-playing"
        headers = {"Authorization": f"Bearer {spotify_token}"}
        playback_response = requests.get(playback_url, headers=headers)

        if playback_response.status_code != 200:
            return JsonResponse({"error": "Could not fetch playback data"}, status=400)

        playback_data = playback_response.json()
        if not playback_data or "item" not in playback_data:
            return JsonResponse({"error": "No track is currently playing"}, status=404)

        track_uri = playback_data["item"]["uri"]
        progress_ms = playback_data["progress_ms"]

        members = group.members.exclude(id=user.id).filter(spotify_token__isnull=False)

        if not members:
            return JsonResponse({"error": "No users available for synchronization"}, status=404)

        for member in members:
            headers = {"Authorization": f"Bearer {member.spotify_token}"}
            play_url = "https://api.spotify.com/v1/me/player/play"
            data = {
                "uris": [track_uri],
                "position_ms": progress_ms
            }
            requests.put(play_url, headers=headers, json=data)

        return JsonResponse({"message": "Playback synchronized successfully"})
    
    
SPOTIFY_API_URL = "https://api.spotify.com/v1"

class CreatePlaylistView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        current_user = request.user  # Utilisateur qui fait la requête
        target_username = request.data.get("username")  # Utilisateur dont on veut la playlist

  
        try:
            target_user = User.objects.get(username=target_username)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        try:
            group = Group.objects.get(members=current_user, members=target_user)
        except Group.DoesNotExist:
            return JsonResponse({"error": "Users are not in the same group"}, status=403)

        if not target_user.spotify_token:
            return JsonResponse({"error": "Target user has not linked their Spotify account"}, status=403)

        top_tracks_url = f"{SPOTIFY_API_URL}/me/top/tracks?limit=10"
        headers = {"Authorization": f"Bearer {target_user.spotify_token}"}
        response = requests.get(top_tracks_url, headers=headers)

        if response.status_code != 200:
            return JsonResponse({"error": "Failed to fetch top tracks"}, status=400)

        tracks_data = response.json()
        track_uris = [track["uri"] for track in tracks_data.get("items", [])]

        if not track_uris:
            return JsonResponse({"error": "No top tracks found"}, status=404)

        create_playlist_url = f"{SPOTIFY_API_URL}/me/playlists"
        playlist_data = {
            "name": f"Top 10 Songs of {target_username}",
            "description": "Generated by SpotYnov API",
            "public": False
        }
        create_response = requests.post(create_playlist_url, headers=headers, json=playlist_data)

        if create_response.status_code != 201:
            return JsonResponse({"error": "Failed to create playlist"}, status=400)

        playlist_id = create_response.json()["id"]


        add_tracks_url = f"{SPOTIFY_API_URL}/playlists/{playlist_id}/tracks"
        add_response = requests.post(add_tracks_url, headers=headers, json={"uris": track_uris})

        if add_response.status_code != 201:
            return JsonResponse({"error": "Failed to add tracks"}, status=400)

        return JsonResponse({"message": "Playlist created successfully!", "playlist_id": playlist_id})