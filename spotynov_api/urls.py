from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from users.views import SpotifyLoginView, spotify_callback
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


def home(request):
    return JsonResponse({"message": "Bienvenue sur Spotynov API!"})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # Remplace 'mon_app' par le nom de ton application Django
    path('', home, name='home'),  # Accueil de l'API
]
