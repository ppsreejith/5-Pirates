from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import HttpResponse
from game.models import Profile
import requests

def index(request, message = ''):
    if request.user.is_authenticated():
        return redirect('game')
    return render(request,'index.html',{message:message})

def login(request):
    if request.user.is_authenticated():
        return redirect('game')
    
    # The workflow is: we get the `code` from the get request.
    # We then proceed to exchange it for an `access token` from facebook.
    # We then obtain user info using the `access token` and proceed to
    # either log him in or sign him up.
    
    fb_code = request.GET.get('code')
    try:
        if fb_code is not None:
            token_response = requests.get('https://graph.facebook.com/oauth/access_token?client_id=414682281965382&redirect_uri=http://ppsreejith.ktj.in:8000/login/&client_secret=aa6b5e6eb4399581d7fc00e0cbc3eb93&code=%s'%fb_code).content
	    token_response = token_response.split('&')[0]
            user_data = requests.get('https://graph.facebook.com/me?scope=email&%s'%token_response).json()
            if 'error' in user_data:
                raise Exception("Error in retrieving data")
            try:
                profile = Profile.objects.get(facebook_id = user_data['id'])
            except Exception:
                user = User.objects.create_user(user_data['username'],user_data['email'],user_data['id']+user_data['email'])
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.save()
                profile = Profile(user = user,
                                  facebook_id = user_data['id'])
                profile.save()
                login(request, profile.user)
                return redirect('game')
            else:
                if profile.user.is_active:
                    login(request, profile.user)
                    return redirect('game')
                else:
                    return redirect('index',{'message':'Your account has been deactivated.'})
    except Exception as e:
        return HttpResponse(str(e))
    return redirect('index')
