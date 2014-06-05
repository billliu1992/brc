from django.conf.urls import patterns, include, url

from schedule import views

urlpatterns = patterns('',
	url(r'^$', 'schedule.views.all_schedules_page'),
	url(r'^new/$', 'schedule.views.new_schedule'),
	url(r'^(?P<schedule>\w+)/$', 'schedule.views.view_schedule_page'),
	url(r'^(?P<schedule>\w+)/edit/$', 'schedule.views.edit_schedule_page'),
	url(r'^(?P<schedule>\w+)/edit/submit_schedule/$', 'schedule.views.submit_schedule'),
	url(r'^(?P<schedule>\w+)/join/$', 'schedule.views.join_schedule'),
	url(r'^(?P<schedule>\w+)/leave/$', 'schedule.views.leave_schedule'),
)
