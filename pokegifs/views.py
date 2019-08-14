from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
# from .forms import *
from .models import *
import requests 
import json 
import os 
from django.http import JsonResponse 
import dotenv 
import socket 



def root(request): 
    return redirect('home/')
    
def home(request): 
    return render(request, 'index.html')
    
def pokemon_show(request, pk): 
    try: 

        api_url = f"http://pokeapi.co/api/v2/pokemon/{pk}/"
        res = requests.get(api_url) 
        body = json.loads(res.content) 
        poke_name = body['name']
        poke_id = body['id']
        poke_type = body['types'][0]['type']['name']

        giphy_api_key = os.environ.get('GIPHY_API_KEY')
        query = poke_name
        limit = 1
        offset = 0
        rating = 'G'   
        giphy_url = f"https://api.giphy.com/v1/gifs/search?api_key={giphy_api_key}&q={query}&limit={int(limit)}&offset={int(offset)}&rating={rating.upper()}&lang=en"
    
        giphy_res = requests.get(giphy_url)
        giphy_body = json.loads(giphy_res.content) 
        
        # data = giphy_res.json() 
        data = giphy_body['data'][0]
        gif = data['images']['fixed_height']['url'] 
    
    except ValueError: 
        return HttpResponse('Pokemon not found.')
    except NameError: 
        return HttpResponse("Invalid Key")

    return JsonResponse({"name": poke_name, "id": poke_id, "type": poke_type, "gif": gif  })

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            
            username = form.cleaned_data['username']
            pw = form.cleaned_data['password']
            user = authenticate(username=username, password=pw)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home')
            else:
                form.add_error('username', 'Login failed')
    else:
        form = LoginForm()

    return render(request, 'login.html', {
        'form': form
    }) 


def signup(request):
    form = UserCreationForm() 
    context =  {'form': form} 
    return render(request, 'registration/signup.html', context)

def signup_create(request): 
    form = UserCreationForm(request.POST)
    if form.is_valid(): 
        new_user = form.save()
        login(request, new_user)
        return redirect('/')
    else: 
        return render(request, 'registration/signup.html', {'form': form})
