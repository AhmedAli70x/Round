from django.urls import path
from .views import RegistrationView, ListUsers


urlpatterns = [
    path('api/register/', RegistrationView.as_view(), name='api_register'),
    path('api/list_users/', ListUsers.as_view(), name='list_users'),


]