# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

def index(request):
    if request.user.is_authenticated():
        return redirect('game')
    return render(request,'index.html',{})

def login(request):
    if request.user.is_authenticated():
        return redirect('game')
    
    # The workflow is: we get the `code` from the get request.
    # We then proceed to exchange it for an `access token` from facebook.
    # We then obtain user info using `access token` and proceed to
    # either log him in or sign him up.
    
    fb_code = request.GET.get('code')
    try:
        if fb_code is not None:
            token_response = requests.get('https://graph.facebook.com/oauth/access_token?client_id=414682281965382&redirect_uri=http://ppsreejith.ktj.in:8000/login/&client_secret=aa6b5e6eb4399581d7fc00e0cbc3eb93&code=%s'%fb_code).content
	    token_response = token_response.split('&')[0]
            user_data = requests.get('https://graph.facebook.com/me?scope=email&%s'%token_response).content
            return HttpResponse(user_data)
    except Exception as e:
        return HttpResponse(str(e))
    return redirect('index')

def game(request):
    return render(request,'game.html',{})
