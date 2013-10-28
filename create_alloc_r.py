from game.models import Profile, RoundAllotment

def get_cycle(no):
    if(no > 20):
        no = no - 21
    return no
    

def create_alloc(sess):
    players = Profile.objects.order_by('rank')[:126]
    k = players.count() / 21 #ignoring surpluses for the moment
    curr_list = []
    for i in range(k):
        curr_list = []
        curr = i
        print "Allotment for group_id=" + str(i)
        for j in range(21):
            curr_list.append(players[curr])
            curr += k
        for j in range(21):
            print curr_list[j].user.username
        #generate allotment with curr_list
        
        for j in range(21):
            n1 = j
            n2 = get_cycle(n1 + 1)
            n3 = get_cycle(n2 + 3)
            n4 = get_cycle(n3 + 10)
            n5 = get_cycle(n4 + 2)
            print("game_id=" + str(j) + " " + str(n1) + ' ' + str(n2) + ' ' + str(n3) + ' ' + str(n4) + ' ' + str(n5))
            rnd = RoundAllotment(pos1=curr_list[n1], pos2=curr_list[n2], pos3=curr_list[n3], pos4=curr_list[n4], pos5=curr_list[n5], session=sess, group_id=i, game_id=j)
            rnd.save()


print 'loaded'
