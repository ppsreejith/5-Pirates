from game.models import RoundAllotment, Round
from django.db.models import Max
import random

def play_session(sess):
    #for all games in gameallotment of this session
    #play game, record scores in gameallotment, update score of player
    #play game involves 
    games = RoundAllotment.objects.order_by('group_id', 'game_id')
    #for game in games:
    game = games[0]
    print str(game.game_id) + " " + str(game.group_id)
    play_game(game)
    

def play_game(game):
    poss_strats = Round.objects.filter(session=game.session)
    strat_list = []
    for curr_posn_cap in range(1, 6):
        curr_list = []
        curr_player = getattr(game, 'pos%d'%curr_posn_cap)
        print curr_player
        for opp_posn in range(1, 6):
            strat = poss_strats.get(player_one=curr_player, position_one=curr_posn_cap, position_two=opp_posn)
            curr_list.append(strat.amount)
        #print curr_list
        strat_list.append(curr_list)
    print strat_list
    #now play game
    scores = []
    for curr_posn_cap in range(1, 6):
        votes = 1
        for oppn_posn in range(curr_posn_cap + 1, 6):
            if strat_list[curr_posn_cap - 1][oppn_posn - 1] >= strat_list[oppn_posn - 1][curr_posn_cap - 1]:
                votes += 1
        players = (6 - curr_posn_cap)
        min = players / 2
        if players % 2 == 1:
            min += 1
        if votes >= min:
            #This distribution is accepted
            print "Distribution of %d has been accepted with %d votes" %(curr_posn_cap, votes)
            for i in range(1, curr_posn_cap):
                scores.append(0)
            for i in range(curr_posn_cap, 6):
                scores.append(strat_list[curr_posn_cap - 1][i - 1])
            print scores
            break
        else:
            print "Distribution of %d has been rejected with %d votes" %(curr_posn_cap, votes)
    
        
            
                            
        
    

def gen_rand_strat(player, posn, sess):
    for i in range(1, posn):
        amt = random.randint(1, 100)
        rnd = Round(player_one=player, position_one=posn, position_two=i, amount=amt, session=sess)
        rnd.save()
    sum = 0
    for i in range(posn, 5):
        no = random.randint(1, 20)
        sum += no
        amt = no
        rnd = Round(player_one=player, position_one=posn, position_two=i, amount=amt, session=sess)
        rnd.save()
    
    rnd = Round(player_one=player, position_one=posn, position_two=5, amount=100-sum, session=sess)
    rnd.save()
    

def generate_trial_rounds(sess):
    games = RoundAllotment.objects.order_by('group_id', 'game_id')
    group_cnt = games.aggregate(Max('group_id'))['group_id__max'] + 1
    #for game in games:
    game = games[0]
    gen_rand_strat(game.pos1, 1, sess)
    gen_rand_strat(game.pos2, 2, sess)                    
    gen_rand_strat(game.pos3, 3, sess)
    gen_rand_strat(game.pos4, 4, sess)
    gen_rand_strat(game.pos5, 5, sess)


        
        
        


print "loaded"
