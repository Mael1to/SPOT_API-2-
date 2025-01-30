from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import User

class RegisterUserView(APIView):
    parser_classes = [JSONParser]  # Forcer la lecture du JSON

    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return Response({"error": "Nom d'utilisateur et mot de passe requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User(username, password)
            user.save()
            return Response({"message": "Utilisateur créé avec succès !"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
