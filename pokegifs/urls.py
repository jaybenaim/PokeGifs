from django.contrib import admin
from django.urls import path, include 
from .views import *

urlpatterns = [
    path('', root), 
    path('admin/', admin.site.urls),
    path('home/', home),
    path('accounts/signup', signup, name='signup'), 
    path('accounts/signup_create', signup_create, name='signup_create'), 
    path('accounts/profile/', include('django.contrib.auth.urls')), 
    path('pokemon/<int:pk>', pokemon_api, name='pokemon_api'),
    path('pokemon/<int:pk>/show', pokemon_show, name='pokemon_show'),
    path('pokemon/search', pokemon_search, name="pokemon_search"), 
    # path('pokemon/team', pokemon_team, name='teams'), 
]