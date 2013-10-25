from django.conf import settings
from core.models import GlobalSettings
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    facebook_id = models.CharField(max_length=20)
    total_points = models.PositiveIntegerField(default=0)
    sessions_without_playing = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default = lambda:Profile.objects.count())

    def __unicode__(self):
        return self.user.username

# Each round, `player_one` in position `position_one` pays/demands
# `amount` money to/from `player_two` in position `position_two`

class Strategy(models.Model):
    position = models.PositiveIntegerField()
    player = models.ForeignKey(Profile,related_name='round_player_one')
    #player_two = models.ForeignKey(Profile,related_name='round_player_two', default=NULL)
    amount1 = models.PositiveIntegerField()
    amount2 = models.PositiveIntegerField()
    amount3 = models.PositiveIntegerField()
    amount4 = models.PositiveIntegerField()
    amount5 = models.PositiveIntegerField()
    
    times = models.PositiveIntegerField(default = 0) #No: of times entries have been edited.
    session = models.PositiveIntegerField() #Current Session Number

    
    class Meta:
        unique_together = (('player','position','session'))


        
    @classmethod
    def create_or_update(cls, playr, posn, sess, amts):
        try:
            strat = cls.objects.get(player=playr, position=posn, session=sess)
        except Exception:
            strat = cls(player=playr, position=posn, session=sess, amount1=amts[0], amount2=amts[1], amount3=amts[2], amount4=amts[3], amount5=amts[4])
        else:
            strat.amount1 = amts[0]
            strat.amount2 = amts[1]
            strat.amount3 = amts[2]
            strat.amount4 = amts[3]
            strat.amount5 = amts[4]
            strat.times += 1
        finally:
            strat.save()
    
    # To create a new round, player_one is passed and then an array
    # of amounts, to the other players, are passed along.
    @classmethod
    def newStrategy(cls,session,position,player,amounts):
        if position < 1 or position > 5:
            raise ValidationError("Position should be in (1,2,3,4,5)")
        if any( n<0 for n in amounts ):
            raise ValidationError("Amount can't be less than zero")
        sum = reduce(lambda x,y: x+y, amounts[position-1:])
        if sum > 100:
            raise ValidationError("You can't give away more than 100 Coins ")
        if len(amounts) != 5:
            raise ValidationError("Exactly 5 amounts have to be specified")
        #players_dict = RoundAllotment.getOtherPlayers(session,position,player)
        cls.create_or_update(player, position, session, amounts)
        

#to be changed
    @classmethod
    def getHisAlloc(cls, session, player): #Get a dictionary showign a players allocation to all his opponents in a round
        strategies = cls.objects.filter(player=player, session=session)
        ret_alloc = []
        try:
            for i in range(1, 6):
                for j in range(1, 6):
                    ret_alloc.append({'userPos':i, 'position':j, 'amount':getattr(strategies.get(position=i), 'amount%d'%j)})
        except Exception:
            return []
        else:
            return ret_alloc
        
        
                            
                    
        

            

class RoundAllotment(models.Model):
    pos1 = models.ForeignKey(Profile, related_name = 'roundallottment_pos1')
    pos2 = models.ForeignKey(Profile, related_name = 'roundallottment_pos2')
    pos3 = models.ForeignKey(Profile, related_name = 'roundallottment_pos3')
    pos4 = models.ForeignKey(Profile, related_name = 'roundallottment_pos4')
    pos5 = models.ForeignKey(Profile, related_name = 'roundallottment_pos5')
    session = models.PositiveIntegerField()

    group_id = models.PositiveIntegerField()
    game_id = models.PositiveIntegerField()

    sco1 = models.PositiveIntegerField(default=0)
    sco2 = models.PositiveIntegerField(default=0)
    sco3 = models.PositiveIntegerField(default=0)
    sco4 = models.PositiveIntegerField(default=0)
    sco5 = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.pos1.user.username
    
    class Meta:
        unique_together = (('pos1','pos2','pos3','pos4','pos5','session'))
    
    @classmethod
    def checkValid(cls,session,pos1,player1,pos2,player2):
        if (pos1 == pos2) or (player1 == player2): return False;
        
        return cls.objects.filter(**{ 'pos%d'%pos1 : player1,
                                      'pos%d'%pos2 : player2,
                                      'session' : session }).exists()
    
    @classmethod
    def getOtherPlayers(cls, session, position, player):
        alottment = cls.objects.get({ 'pos%d'%position : player,
                                      'session' : session })
        players_dict = {}
        
        # The code below loops though the current
        # allotment, finding all other players of the same
        # allotment and returning a dictionary.
        
        for i in range(1,6):
            if i == position:
                continue
            players_dict[i] = getattr(allotment,'pos%d'%i)
        
        return players_dict
        
    @classmethod
    def getAllPlayerStars(cls, session, player):
        player_count = Profile.objects.count()
        players = []
        Q = models.Q
        alottment = cls.objects.filter( Q(pos1 = player) |
                                        Q(pos2 = player) |
                                        Q(pos3 = player) |
                                        Q(pos4 = player) |
                                        Q(pos5 = player),
                                        session = session )
        for i in range(1,6):
            alott = alottment.get(**{ 'pos%d'%i : player })
            pos1 = getattr( alott,'pos%d'%(i%5+1) )
            pos2 = getattr( alott,'pos%d'%((i+1)%5+1) )
            pos3 = getattr( alott,'pos%d'%((i+2)%5+1) )
            pos4 = getattr( alott,'pos%d'%((i+3)%5+1) )
            players.extend([{'position':i%5+1,'userPos':i,'stars':cls.starrify(pos1.rank)},
                            {'position':(i+1)%5+1,'userPos':i,'stars':cls.starrify(pos2.rank)},
                            {'position':(i+2)%5+1,'userPos':i,'stars':cls.starrify(pos3.rank)},
                            {'position':(i+3)%5+1,'userPos':i,'stars':cls.starrify(pos4.rank)}])
        return players


    @classmethod
    def starrify(cls, rank):
        player_count = Profile.objects.count()
        num = (rank - 1) * 3
        ret = num / player_count
        ret = 3 - ret
        return ret
