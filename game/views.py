# Create your views here.
from django.shortcuts import render, redirect
from djanog.http import HTTPResponse
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
    # We then obtain user info using access token and proceed to
    # either log him in or sign him up.
    
    fb_code = request.GET.get('code')
    try:
        if fb_code is not None:
            token_reponse = requests.get('https://graph.facebook.com/oauth/access_token?client_id=414682281965382&redirect_uri=http://localhost:8000/login/&client_secret=aa6b5e6eb4399581d7fc00e0cbc3eb93&code=%s'%fb_code).json()
            user_data = requests.get('https://graph.facebook.com/me?access_token=%s'%token_reponse['access_token']).content
            return HTTPResponse(user_data)
    except Exception:
        pass
    return redirect('index')
