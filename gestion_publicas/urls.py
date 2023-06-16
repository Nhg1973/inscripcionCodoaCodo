from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',home, name='home'),
    path('login/',logIn, name='logIn'),
    path('register/',register, name='register'),
    path('logout/',logOut, name='logOut'),
    path('forgot-password/',forgot, name='forgot'),
]