from game.models import Profile


def reflect():
    players = Profile.objects.order_by('total_points').reverse()
    cnt = 0
    for player in players:
        cnt += 1
        player.rank = cnt
        player.save()

def remove_useless():
    players = Profile.objects.all()

def print_finalists():
    players = Profile.objects.order_by('rank')[:66]
    cnt = 0
    print '%4s %35s %30s %6s' %('Rank', 'Name', 'Username', 'Points')
    for player in players:
        cnt += 1
        if player.user.username == 'bikemaster68882' or player.user.username == 'ppsreejith' or player.user.username == 'manojgadia':
            cnt -= 1
            continue
        print '%4d %35s %30s %6d' %(cnt, player.user.first_name + ' ' +  player.user.last_name, player.user.username, player.total_points)
    
    
print "loaded"
