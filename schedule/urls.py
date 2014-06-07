from django.conf.urls import patterns, include, url

from schedule import views

urlpatterns = patterns('',
	url(r'^$', 'schedule.views.all_schedules_page'),
	url(r'^new/$', 'schedule.views.new_schedule'),
	url(r'^view/(?:(?P<keywords>\w+)/(?P<page_num>\d+)/(?P<num_per_page>\d+))?$', 'schedule.views.view_schedules_list'),
	url(r'^(?P<schedule_pk>\d+)/$', 'schedule.views.view_schedule_page'),
	url(r'^(?P<schedule_pk>\d+)/edit/$', 'schedule.views.edit_schedule_page'),
	url(r'^(?P<schedule_pk>\d+)/edit/submit_schedule/$', 'schedule.views.submit_schedule'),
	url(r'^(?P<schedule_pk>\d+)/join/$', 'schedule.views.join_schedule'),
	url(r'^(?P<schedule_pk>\d+)/leave/$', 'schedule.views.leave_schedule'),
)
