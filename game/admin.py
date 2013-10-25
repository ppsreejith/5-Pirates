from django.contrib import admin
from game.models import Profile, Round, RoundAllotment

class RoundAllotmentAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'game_id', 'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'session')

class RoundAdmin(admin.ModelAdmin):
    list_display = ('position_one', 'position_two', 'player_one', 'amount', 'times', 'session')



admin.site.register(Profile)
admin.site.register(Round, RoundAdmin)
admin.site.register(RoundAllotment, RoundAllotmentAdmin)
