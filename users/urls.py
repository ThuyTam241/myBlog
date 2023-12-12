from django.urls import path
from .views import RegisterView
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', auth_views.LoginView.as_view(template_name='users/profile_user.html'), name='profile'),
    path('logout/', views.logout_user, name='logout'),
]