from game.models import RoundAllotment, Round
from django.db.models import Max
import random

def play_session(sess):
    #for all games in gameallotment of this session
    #play game, record scores in gameallotment, update score of player
    #play game involves 
    games = RoundAllotment.objects.order_by('group_id', 'game_id')
    for game in games:
        print str(game.game_id) + " " + str(game.group_id)

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
play_session(1)
