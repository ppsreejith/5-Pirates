from django.shortcuts import render, redirect

def game(request):
    if not request.user.is_authenticated():
        return redirect('index')
    return render(request,'game.html',{})
