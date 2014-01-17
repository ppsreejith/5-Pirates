from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login as auth_login
from django.http import HttpResponse
from core.models import GlobalValues
from game.models import Profile
from urllib2 import Request,urlopen
import json

def index(request,message = ''):
    glo = GlobalValues.objects.get()
    if not glo.running:
        if not message:
            message = request.user.username + 'The next session will start soon. <a target="_blank" href="https://www.facebook.com/The.KGTS." style="color:lightblue;">Follow us on facebook</a>'
        return render(request,'index.html',{'message':message,'glo':glo})
    if request.user.is_authenticated():
        return redirect('game')
    return render(request,'index.html',{'message':message,'glo':glo})

def login(request):
    
    glo = GlobalValues.objects.get()
    #OYE!! LOOK OVER HERE!!!!! SREEJITH!!
    #Use glo in registration, you need to check these:
    # If session is inactive, don't allow people to login.
    # If allowReg (a new variable) is false, dont allow registrations either.
    
    # The workflow is: we get the `code` from the get request.
    # We then proceed to exchange it for an `access token` from facebook
    # We then obtain user info using the `access token` and proceed to
    # either log him in or sign him up.
    if not glo.running and not glo.allowReg:
        return redirect('index')
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
                if not glo.allowReg:
                    return redirect('index_m', message = 'No more registrations allowed.')
                user = User.objects.create_user(user_data['username'],user_data['email'],'sreejithhere')
                
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.save()
                profile = Profile(user = user,
                                  facebook_id = user_data['id'])
                profile.save()
                user_login = authenticate(username = user.username,
                                          password = 'sreejithhere')
                auth_login(request, user_login)
                return redirect('game')
            else:
                if not glo.running:
                    return redirect('index_m', message = 'Login not allowed till next session starts.')
                if profile.user.is_active:
                    user_login = authenticate(username = profile.user.username, password = 'sreejithhere')
                    auth_login(request, user_login)
                    return redirect('game')
                else:
                    return redirect('index_m', message = 'Your account has been deactivated.')
    except Exception as e:
	return redirect('index')
    return redirect('index')
