# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginView, ProfileView, FollowToggleView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),        # custom login (returns token)
    path('token-auth/', obtain_auth_token, name='token_auth'),# DRF built-in token endpoint (optional)
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/follow/', FollowToggleView.as_view(), name='follow-toggle'),
]
