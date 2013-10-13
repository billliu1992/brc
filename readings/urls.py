from django.conf.urls import patterns, include, url

from readings import views

urlpatterns = patterns('',
	url(r'^$', 'readings.views.readings_page'),
	url(r'^submit_reading', 'readings.views.add_reading'),
	url(r'^delete_reading/(?P<reading>\w+)/(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)', 'readings.views.delete_reading')
)
