from django.conf.urls import patterns, include, url

from encourage import views

urlpatterns = patterns('',
	url(r'^$', 'encourage.views.main_page'),
	url(r'^view/(?:(?P<keywords>\w+)/(?P<page_num>\d+)/(?P<num_per_page>\d+))?$', 'encourage.views.challenge_list'),
	url(r'^create/$', 'encourage.views.create_challenge'),
	url(r'^page/(?P<challenge_pk>\w+)/$', 'encourage.views.challenge_page'),
	url(r'^join/(?P<challenge_pk>\w+)/(?P<team_pk>\w+)$', 'encourage.views.join_team')
)
