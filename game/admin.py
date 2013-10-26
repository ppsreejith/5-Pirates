from django.contrib import admin
from game.models import Profile, Strategy, RoundAllotment

class RoundAllotmentAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'game_id', 'pos1', 'pos2', 'pos3', 'pos4', 'pos5', 'session', 'sco1', 'sco2', 'sco3', 'sco4', 'sco5')

class StrategyAdmin(admin.ModelAdmin):
    list_display = ('player', 'position', 'amount1', 'amount2', 'amount3', 'amount4', 'amount5','times', 'session')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'facebook_id', 'total_points', 'sessions_without_playing', 'rank')


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Strategy, StrategyAdmin)
admin.site.register(RoundAllotment, RoundAllotmentAdmin)
