from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.index', name='index'),
    url(r'^m/(?P<message>.*)$', 'core.views.index', name='index_m'),
    url(r'^login', 'core.views.login', name='login'),
    url(r'^game$', 'game.views.game', name='game'),
    #url(r'^results$',TemplateView.as_view(template_name='results.html')),
    url(r'^allapaq$', 'game.views.secret_game'),
    # url(r'^pirates/', include('pirates.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^game/pirates', 'game.views.stars', name='stars'),
    url(r'^game/tables', 'game.views.get_allocation', name='getalloc'),
    url(r'^game/setalloc', 'game.views.set_allocation', name='setalloc'),
    url(r'^game/leaderboard', 'game.views.get_leaderboard', name='leaderboard'),
    url(r'^game/score', 'game.views.get_score', name='score'),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
                       
)
