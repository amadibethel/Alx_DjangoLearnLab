from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # auth
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # built-in views for login/logout
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),

    # example index placeholder
    path('', views.index, name='index'),  # ensure you have an index view or change accordingly
]
