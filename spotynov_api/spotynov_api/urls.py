from django.contrib import admin
from django.urls import path, include
from users.views import (
    RegisterView, LoginView, CustomTokenRefreshView,
    CreateGroupView, JoinGroupView, LeaveGroupView, ListGroupsView,
    SpotifyAuthView, SpotifyCallbackView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  


    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("groups/create/", CreateGroupView.as_view(), name="create_group"),
    path("groups/join/", JoinGroupView.as_view(), name="join_group"),
    path("groups/leave/", LeaveGroupView.as_view(), name="leave_group"),
    path("groups/", ListGroupsView.as_view(), name="list_groups"),

    path("spotify/auth/", SpotifyAuthView.as_view(), name="spotify_auth"),
    path("spotify/callback/", SpotifyCallbackView.as_view(), name="spotify_callback"),
    
    path("callback/", SpotifyCallbackView.as_view(), name="spotify_callback_redirect"),
]
