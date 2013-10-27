from game.models import Profile


def reflect():
    players = Profile.objects.order_by('total_points').reverse()
    cnt = 0
    for player in players:
        cnt += 1
        player.rank = cnt
        player.save()
    
print "loaded"
