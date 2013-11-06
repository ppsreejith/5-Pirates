from game.models import Profile, RoundAllotment, Strategy

def keep_top63():
    players = Profile.objects.order_by('total_points').reverse()
    cnt = 0
    for player in players:
        if player.user.username == 'ppsreejith' or player.user.username == 'manojgadia' or player.user.username == 'bikemaster68882' or player.user.username == 'niteshsekhar' or player.user.username == 'abhishek.bhowmick.378' or cnt >= 63:
            player.delete()
        else:
            cnt += 1

def clear_tables():
    allots = RoundAllotment.objects.all()
    for allotment in allots:
        allotment.delete()
    strats = Strategy.objects.all()
    for strat in strats:
        strat.delete()



print 'loaded'
