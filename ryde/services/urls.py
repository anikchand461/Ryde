# services/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('setup-profile/', views.setup_profile, name='setup_profile'),
    path('provider-profile/', views.view_provider_profile, name='provider_profile'),
]