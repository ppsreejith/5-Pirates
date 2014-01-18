import create_alloc_r
import play_game_r
import reflect_ranks
from core.models import GlobalSettings

SESSION = 7

def go():
    setting = GlobalSettings.objects.get()
    SESSION = setting.current_session
    play_game_r.getAvgStrategies(SESSION)
    play_game_r.play_session(SESSION)
    reflect_ranks.reflect()
    create_alloc_r.create_alloc(SESSION + 1)
    setting.current_session = SESSION + 1
    setting.save()
