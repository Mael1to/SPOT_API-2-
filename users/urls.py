from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, LoginView, ProtectedView,
    GroupListView, GroupUsersView, CreateGroupView, JoinGroupView, LeaveGroupView,
    UserPersonalityView, SyncPlaybackView, SpotifyTokenView
)
from users.views import SpotifyLoginView, spotify_callback
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SpotYnov API",
        default_version='v1',
        description="Documentation de l'API SpotYnov",
        terms_of_service="https://www.spotify.com/legal/end-user-agreement/",
        contact=openapi.Contact(email="contact@spotynov.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Auth & Token Management
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Group Management
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/create/', CreateGroupView.as_view(), name='create_group'),
    path('groups/join/', JoinGroupView.as_view(), name='join_group'),
    path('groups/<str:group_name>/users/', GroupUsersView.as_view(), name='group-users'),
    path('groups/leave/', LeaveGroupView.as_view(), name='leave_group'),
    path('groups/sync/', SyncPlaybackView.as_view(), name='sync-playback'),
    
    # User & Spotify Management
    path('users/<str:username>/personality/', UserPersonalityView.as_view(), name='user-personality'),
    path('spotify/tokens/<str:username>/', SpotifyTokenView.as_view(), name='spotify-tokens'),
    path("spotify/login/<str:username>/", SpotifyLoginView.as_view(), name="spotify-login"),
    path('spotify/callback/', spotify_callback, name='spotify-callback'),
    path('spotify/login/<str:username>/', SpotifyLoginView.as_view(), name='spotify-login'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
