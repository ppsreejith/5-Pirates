from django.shortcuts import render, redirect
from django.http import HttpRequest
from game.models import RoundAllotment
from core.models import GlobalSettings
from django.utils import simplejson

def json_response(something):
    return HttpResponse(
        simplejson.dumps(something),
        content_type = 'application/javascript; charset=utf8'
    )

def game(request):
    if not request.user.is_authenticated():
        return redirect('index')
    return render(request,'game.html',{})

def stars(request):
    session = GlobalSettings.get().current_session
    player = Profile.objects.get(user__username=request.user)
    star_dict = RoundAllotment.getAllPlayerStars(session, player)
    return json_response(star_dict)

def get_allocation(request):
    session = GlobalSettings.get().current_session
    player = Profile.objects.get(user__username=request.user)
    alloc_dict = Strategy.getHisAlloc(session, player)
    return json_response(alloc_dict)

def set_allocation(request):
    session = GlobalSettings.get().current_session
    player = Profile.objects.get(user__username=request.user)
    data = request.POST.copy()
    amounts = []
    posn = data['pos']
    amounts.append(data['val1'])
    amounts.append(data['val2'])
    amounts.append(data['val3'])
    amounts.append(data['val4'])
    sum = 0
    for i in range(posn - 1, 5):
        sum += amounts[i]
    amounts.append(100 - sum)
    Strategy.newStrategy(session, posn, player, amounts)
    return HttpResponse("")
    
        
        
