from django.contrib import admin
from django.urls import path
from app_all.views import weather_api

urlpatterns = [
    path('api/<city>', weather_api),
]
