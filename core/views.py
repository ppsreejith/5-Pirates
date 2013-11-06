from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.http import HttpResponse
from core.models import GlobalValues
from game.models import Profile
from urllib2 import Request,urlopen
import json

def index(request,message = ''):
    #if request.user.is_authenticated():
     #  message = request.user.username + ', You have been registered. The preliminary round has ended. Follow us on facebook. https://www.facebook.com/The.KGTS.'
    #    return redirect('game')
    glo = GlobalValues.objects.get()
    return render(request,'index.html',{'message':message,'glo':glo})

def login(request):
    
    # The workflow is: we get the `code` from the get request.
    # We then proceed to exchange it for an `access token` from facebook3
    # We then obtain user info using the `access token` and proceed to
    # either log him in or sign him up.
    
    redirect_uri = 'http://brethren.kgts.in:9000/login/'
    
    fb_code = request.GET.get('code')
    try:
        if fb_code is not None:
            r = urlopen(Request('https://graph.facebook.com/oauth/access_token?client_id=414682281965382&redirect_uri=%s&client_secret=aa6b5e6eb4399581d7fc00e0cbc3eb93&code=%s'%(redirect_uri,fb_code)))
            token_response = r.read()
	    token_response = token_response.split('&')[0]
            user_data = json.load(urlopen(Request('https://graph.facebook.com/me?scope=email&%s'%token_response)))
            
            if 'error' in user_data:
                raise Exception("Error in retrieving data")
            
            try:
                profile = Profile.objects.get(facebook_id = user_data['id'])
            except Exception:
                #user = User.objects.create_user(user_data['username'],user_data['email'],'sreejithhere')
                
                #user.first_name = user_data['first_name']
                #user.last_name = user_data['last_name']
                #user.save()
                #profile = Profile(user = user,
                                  #facebook_id = user_data['id'])
                #profile.save()
                #user_login = authenticate(username = user.username,
                                          #password = 'sreejithhere')
                #auth_login(request, user_login)
                #return redirect('game')
                return redirect('index')
            else:
                if profile.user.is_active:
                    user_login = authenticate(username = profile.user.username,
                                              password = 'sreejithhere')
                    auth_login(request, user_login)
                    #return redirect('game')
                    return redirect('index')
                else:
                    return redirect('index_m', message = 'Your account has been deactivated.')
    except Exception as e:
        #return HttpResponse(str(e))
	return redirect('index')
    return redirect('index')
