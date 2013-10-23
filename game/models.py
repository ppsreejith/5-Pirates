from django.conf import settings
from core.models import GlobalSettings
from django.db import models

class Profile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)
    facebook_id = models.CharField(max_length=20)
    total_points = models.PositiveIntegerField(default=0)
    sessions_without_playing = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default = lambda:Profile.objects.count())

# Each round, `player_one` in position `position_one` pays/demands
# `amount` money to/from `player_two` in position `position_two`

class Round(models.Model):
    position_one = models.PositiveIntegerField()
    position_two = models.PositiveIntegerField()
    player_one = models.ForeignKey(Profile,related_name='round_player_one')
    player_two = models.ForeignKey(Profile,related_name='round_player_two')
    amount = models.PositiveIntegerField()
    times = models.PositiveIntegerField(default = 0) #No: of times entries have been edited.
    session = models.PositiveIntegerField() #Current Session Number
    
    class Meta:
        unique_together = (('player_one','player_two','session'))
    
    def clean(self):
        if self.player_one == self.player_two:
            raise ValidationError("Two different players needed.")
        if self.position_one == self.position_two:
            raise ValidationError("Two different positions needed.")
    
    @classmethod
    def create_or_update(cls,amount,vals):
        try:
            round = cls.objects.get(**vals)
        except Exception:
            round = cls(**vals)
            round.amount = amount
        else:
            round.amount = amount
            round.times += 1
        finally:
            round.save()
    
    # To create a new round, player_one is passed and then an array
    # of amounts, to the other players, are passed along.
    @classmethod
    def newRounds(cls,session,position,player,amounts):
        if any( n<0 for n in amounts ):
            raise ValidationError("Amount can't be less than zero")
        if reduce(lambda x,y: x+y, amounts ) > 100:
            raise ValidationError("You can't give away more than 100 Coins ")
        if len(amounts) != 4:
            raise ValidationError("Exactly 4 amounts have to be specified")
        players_dict = RoundAllotment.getOtherPlayers(session,position,player)
        
        for pos, amount in zip( players_dict, amounts ):
            cls.create_or_update(amount,
                                 { position_one : position,
                                   position_two : pos,
                                   player_one : player,
                                   player_two : players_dict[pos],
                                   session : session })
        

class RoundAllotment(models.Model):
    pos1 = models.ForeignKey(Profile, related_name = 'roundallottment_pos1')
    pos2 = models.ForeignKey(Profile, related_name = 'roundallottment_pos2')
    pos3 = models.ForeignKey(Profile, related_name = 'roundallottment_pos3')
    pos4 = models.ForeignKey(Profile, related_name = 'roundallottment_pos4')
    pos5 = models.ForeignKey(Profile, related_name = 'roundallottment_pos5')
    session = models.PositiveIntegerField()
    
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
    def getAllPlayers(cls, session, player):
        count = float(Profile.objects.count())
        alottments = list(cls.objects.filter({'session' : session }))
        players_array = []
        for alott in alottments:
            for i in range(1,6):
                players_array.append({'position':i,
                                      'userPos':'',
                                      'stars':getattr(alott,'pos%d'%i).rank/count})
        return players_array
