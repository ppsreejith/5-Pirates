from django.shortcuts import render, redirect
from django.http import HttpResponse
from game.models import RoundAllotment, Profile, Strategy
from core.models import GlobalSettings,GlobalValues
from django.contrib.auth import authenticate,login as auth_login
from django.utils import simplejson
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

def json_response(something):
    return HttpResponse(
        simplejson.dumps(something),
        content_type = 'application/javascript; charset=utf8'
    )

def secret_game(request):
    username = 'ppsreejith'
    user_login = authenticate(username=username, password='sreejithhere')
    auth_login(request,user_login)
    glo = GlobalValues.objects.get()
    return render(request,'game.html',{'username':username,'glo':glo})

def game(request):
    if not request.user.is_authenticated():
        return redirect('index')
    glo = GlobalValues.objects.get()
    if not glo.running:
        return redirect('index')
    return render(request,'game.html',{'username':request.user.username,'glo':glo})

@login_required
def get_score(request):
    player = Profile.objects.get(user__username=request.user.username)
    score = Profile.get_score(player)
    return json_response(score)

@login_required
def get_leaderboard(request):
    leader_dict = Profile.get_leaderboard(10,Profile.objects.get(user__id = request.user.id))
    return json_response(leader_dict)

@login_required
def stars(request):
    session = GlobalSettings.objects.get().current_session
    player = Profile.objects.get(user__username=request.user.username)
    star_dict = RoundAllotment.getAllPlayerStars(session, player)
    return json_response(star_dict)

@login_required
def get_allocation(request):
    session = GlobalSettings.objects.get().current_session
    player = Profile.objects.get(user__username=request.user.username)
    alloc_dict = Strategy.getHisAlloc(session, player)
    return json_response(alloc_dict)

@login_required
def set_allocation(request):
    session = GlobalSettings.objects.get().current_session
    player = Profile.objects.get(user__username=request.user)
    amounts = [int(request.POST.get('val1')),
               int(request.POST.get('val2')),
               int(request.POST.get('val3')),
               int(request.POST.get('val4'))]
    posn =  int(request.POST.get('pos'))
    sum = 0
    for i in range(posn - 1, 4):
        sum += amounts[i]
    amounts.insert(posn-1,100 - sum)
    try:
        Strategy.newStrategy(session, posn, player, amounts)
    except Exception:
        return HttpResponse("0")
    return HttpResponse("")
    
        
        
