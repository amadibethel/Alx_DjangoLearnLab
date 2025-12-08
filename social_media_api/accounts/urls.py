# accounts/urls.py

from django.urls import path
from .views import feed
from .views import RegisterView, LoginView, ProfileView, FollowToggleView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),        # custom login (returns token)
    path('token-auth/', obtain_auth_token, name='token_auth'),# DRF built-in token endpoint (optional)
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow'),

    path("feed/", feed, name="feed"),    
    path("follow/<int:user_id>/", views.follow_user, name="follow-user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow-user"),
]
