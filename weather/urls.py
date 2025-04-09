from django.urls import path
from . import views

urlpatterns = [
    path('', views.weather, name='weather'),  # Root path for the weather view
]
