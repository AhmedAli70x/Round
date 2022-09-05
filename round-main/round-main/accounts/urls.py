from django.urls import path
from .views import RegistrationView, ListUsers,  LoginView, LogoutView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('list_users/', ListUsers.as_view(), name='list_users'),
    path('token_refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

]