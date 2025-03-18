from django.urls import path
from .views import ( RegisterView, LoginView, ProtectedView, CustomTokenRefreshView, CreateGroupView, JoinGroupView, ListGroupsView, ListGroupMembersView, LeaveGroupView, UserPersonalityView )
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SyncPlaybackView
from .views import CreatePlaylistView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('protected/', ProtectedView.as_view(), name='protected'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += [
    path('groups/create/', CreateGroupView.as_view(), name='create_group'),
    path('groups/join/', JoinGroupView.as_view(), name='join_group'),
    path('groups/', ListGroupsView.as_view(), name='list_groups'),
    path('groups/<str:group_name>/', ListGroupMembersView.as_view(), name='list_group_members'),
    path('groups/leave/', LeaveGroupView.as_view(), name='leave_group'),
]

urlpatterns += [
    path('personality/', UserPersonalityView.as_view(), name='user_personality'),
    path('sync/', SyncPlaybackView.as_view(), name='sync_playback'), 
     path('playlist/create/', CreatePlaylistView.as_view(), name='create_playlist'),
]

