import create_alloc_r
import play_game_r
import reflect_ranks
from core.models import GlobalSettings

def go():
    SESSION = GlobalSettings.objects.get().current_session
    play_game_r.getAvgStrategies(SESSION)
    play_game_r.play_session(SESSION)
    reflect_ranks.reflect()
    create_alloc_r.create_alloc(SESSION + 1)
    GlobalSettings.objects.update(current_session = SESSION + 1)
