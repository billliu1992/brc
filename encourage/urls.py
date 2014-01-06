from django.conf.urls import patterns, include, url

from encourage import views

urlpatterns = patterns('',
	url(r'^$', 'encourage.views.get_reading_schedule_consistency')
)
