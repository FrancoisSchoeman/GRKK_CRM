from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'authentication'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='authentication/login.html', next_page='/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='authentication/password_reset.html'), name='password_reset'),
]