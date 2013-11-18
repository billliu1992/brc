from django.conf.urls import patterns, include, url

from readings import views

urlpatterns = patterns('',
	url(r'^$', 'readings.views.readings_page'),
	url(r'^submit_reading', 'readings.views.add_reading'),
	url(r'^delete_reading/(?P<reading>\w+)/(?P<month>\d+)/(?P<day>\d+)/(?P<year>\d+)', 'readings.views.delete_reading'),
	url(r'^schedules/$', 'readings.views.readings_schedule_page'),
	url(r'^schedules/new/$', 'readings.views.new_schedule'),
	url(r'^schedules/(?P<schedule>\w+)/$', 'readings.views.edit_schedule_page'),
	url(r'^schedules/(?P<schedule>\w+)/submit_schedule/$', 'readings.views.submit_schedule'),
	url(r'^schedules/(?P<schedule>\w+)/join/$', 'readings.views.join_schedule'),
	url(r'^schedules/(?P<schedule>\w+)/leave/$', 'readings.views.leave_schedule'),
)
