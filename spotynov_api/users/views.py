from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserManager, GroupManager

from django.conf import settings

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed



class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = UserManager.create_user(username, password)
        if "error" in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        return Response(result, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Tous les champs sont requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = UserManager.authenticate_user(username, password)
        
        if "error" in result:
            return Response(result, status=status.HTTP_401_UNAUTHORIZED)
     
        user_id = hash(username) % (10**8)  

        
        refresh = RefreshToken()
        refresh["user_id"] = user_id  
        refresh["username"] = username

        return Response({
            "message": "Connexion réussie.",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)



class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Accès autorisé, tu es authentifié !"}, status=status.HTTP_200_OK)


class CustomTokenRefreshView(APIView):
    """
    Gère le renouvellement du token sans base de données.
    """
    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token requis"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            username = refresh.get("username", None)

            if not username:
                raise AuthenticationFailed({"detail": "Utilisateur introuvable", "code": "user_not_found"})

            users = UserManager.load_users()
            if username not in users:
                raise AuthenticationFailed({"detail": "Utilisateur introuvable", "code": "user_not_found"})

            new_access_token = str(refresh.access_token)

            return Response({"access": new_access_token}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "Refresh token invalide"}, status=status.HTTP_401_UNAUTHORIZED)

class CreateGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_name = request.data.get("group_name")
        if not group_name:
            return Response({"error": "Le nom du groupe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = GroupManager.create_group(group_name, request.user.username)
        return Response(result, status=status.HTTP_201_CREATED if "error" not in result else status.HTTP_400_BAD_REQUEST)

class JoinGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group_name = request.data.get("group_name")
        if not group_name:
            return Response({"error": "Le nom du groupe est requis."}, status=status.HTTP_400_BAD_REQUEST)

        result = GroupManager.join_group(group_name, request.user.username)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)

class LeaveGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        result = GroupManager.leave_group(request.user.username)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)

class ListGroupsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = GroupManager.list_groups()
        return Response(result, status=status.HTTP_200_OK)


class ListGroupMembersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_name):
        result = GroupManager.list_group_members(group_name)
        return Response(result, status=status.HTTP_200_OK if "error" not in result else status.HTTP_400_BAD_REQUEST)
