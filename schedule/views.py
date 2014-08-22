import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from schedule.models import ReadingSchedule, ReadingScheduleEntry
from readings.models import *

from parser_util import date_parser, reading_parser

def all_schedules_page(request):
	"""	
	Main page for schedules
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		return redirect('/')
		
	#get the created schedules to put on the view
	created_schedules = ReadingSchedule.objects.filter(creator = request.user)
	
	created_schedules_text = []
	for schedule in created_schedules:
		created_schedules_text.append((schedule.title, schedule.pk))
	
	#get the subscribed schedules	
	subscribed_schedules = request.user.subscribed_sched.all()
	
	subscribed_schedules_text = []
	for schedule in subscribed_schedules:
		subscribed_schedules_text.append((schedule.title, schedule.pk))
	
	#get today's readings
	todays_readings = get_todays_reading(request.user)
	
	context = RequestContext(request, {"created_schedules": created_schedules_text, "subscribed_schedules": subscribed_schedules_text, "todays_readings": todays_readings, "messages": messages})
	return render_to_response('schedule/schedule_main.html', context)
	
def new_schedule(request):
	"""
	Create a new schedule with information from your post data
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		messages.error(request, "Log in to edit this schedule!")
		return redirect('/')
		
	
	context = RequestContext(request, {"new_schedule":True})
	return render_to_response('schedule/edit_reading_schedule.html', context)
	
def view_schedules_list(request, keywords, page_num, num_per_page):
	"""
	Page that displays all the joinable schedules
	"""
	
	if page_num == None:
		page_num = 1
	else:
		try:
			page_num = int(page_num)
		except ValueError:
			page_num = 1
		
	if num_per_page == None:
		num_per_page = 20
	else:
		try:
			num_per_page = int(num_per_page)
		except ValueError:
			num_per_page = 20
	
	all_scheds = ReadingSchedule.objects.all()
	
	schedule_list = None
	
	if(keywords != None):
		schedule_list = []
		
		for sched in all_scheds:
			if keywords.lower() in sched.title.lower():
				schedule_list.append(sched)
	else:
		schedule_list = all_scheds
		
	if(len(schedule_list) < page_num * num_per_page):
		schedule_list = schedule_list[:num_per_page]
	else:
		schedule_list = schedule_list[(page_num-1) * num_per_page : (page_num) * num_per_page]
		
	context = RequestContext(request, {"schedules_list": schedule_list})
	return render_to_response('schedule/schedule_list.html', context)
	
	
	
def view_schedule_page(request, schedule_pk):
	"""
	Page for viewing the schedule
	
	The code for the view splits the schedule into 4 (uneven) columns
	"""
	requested_schedule = ReadingSchedule.objects.get(pk = schedule_pk)
	readings = ReadingEntry.objects.filter(date__gte = requested_schedule.start_date, user = request.user)
	
	print len(readings)
	
	subscribed = requested_schedule in request.user.subscribed_sched.all()
	is_owner = requested_schedule in request.user.created_sched.all()
	
	num_cols = 4
	
	#get the readings to put on the view
	schedule_entries = ReadingScheduleEntry.objects.filter(schedule = requested_schedule)
	
	column_length = len(schedule_entries) / num_cols + 1
	entry_text = []
	for i in range(num_cols):
		entry_text.append([])
	
	
	startdate = requested_schedule.start_date
	for i in range(len(schedule_entries)):
		deadline_date = startdate + datetime.timedelta(days = (schedule_entries[i].day_num - 1))

		column_num = i / column_length
		
		if(subscribed):
			#get whether or not the reading is finished
			reading_status = "unread"
			for reading in readings:
				if(reading.reading == schedule_entries[i].reading):
					#decide whether or not a reading was finished, late, or on time
					reading_deadline = requested_schedule.start_date + datetime.timedelta(schedule_entries[i].day_num)
			
					if(reading.date <= reading_deadline):
						reading_status = "completed"
					elif(reading.date > reading_deadline and reading_status == 0):	#do not want to change an entry that was on time to late if the reading reads a reading twice
						reading_status = "late"
		else:
			reading_status = "grayed"
		
		entry_text[column_num].append((schedule_entries[i].reading, date_parser.parse_date_to_string(deadline_date), reading_status))
	
	context = RequestContext(request, {"title":requested_schedule.title, "all_entries": entry_text, "is_owner": is_owner, "is_subscribed": subscribed})

	return render_to_response('schedule/view_schedule.html', context)
	
	
def edit_schedule_page(request, schedule_pk):
	"""
	Page for editing the schedule
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		messages.error(request, "Log in to edit this schedule!")
		return redirect('/')
		
	#get the schedule
	requested_schedule = ReadingSchedule.objects.get(pk = schedule_pk)
	
	#makes sure that it is the creator
	if(request.user != requested_schedule.creator):
		messages.error(request, "You do not have permission to edit this schedule!")
		return redirect('/schedules/')
	
	#get the readings to put on the view
	schedule_entries = ReadingScheduleEntry.objects.filter(schedule = requested_schedule)
	
	entry_text = []
	for i in range(len(schedule_entries)):
		entry_text.append((i, schedule_entries[i].reading, schedule_entries[i].day_num))
	
	context = RequestContext(request, {"title":requested_schedule.title, "startdate":date_parser.parse_date_to_string(requested_schedule.start_date), "entries":entry_text})
	return render_to_response('schedule/edit_reading_schedule.html', context)
	
def delete_schedule(request, schedule_pk):
	"""
	Delete the schedule
	Will (probably) not delete the schedule from memory, just orphan the schedule
	and allow someone else to take it over
	"""
	return redirect("/schedules/")
	
def submit_schedule(request, schedule_pk):
	"""
	Submit modifications to a schedule
	"""
	
	if(request.method != "POST"):
		return redirect('/schedule')
	
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		messages.error(request, "Log in to edit this schedule!")
		return redirect('/')
	
	new_name = request.POST["name"]
	new_date = request.POST["start_date"]
	num_entries = int(request.POST["entries_num"])
	
	requested_schedule = None
	if(schedule_pk == "0"):
		requested_schedule = ReadingSchedule()
		
		requested_schedule.creator = request.user
	else:
		requested_schedule = ReadingSchedule.objects.get(pk = schedule_pk)
	
		#makes sure that it is the creator
		if(request.user != requested_schedule.creator):
			messages.error(request, "You do not have permission to edit this schedule!")
			return redirect('/schedules/')
	
	requested_schedule.title = new_name
	
	new_date_obj = date_parser.parse_date(new_date)
	if(new_date_obj == None):
		new_date_obj = datetime.date.today()
		
	requested_schedule.start_date = new_date_obj
	
	requested_schedule.save()
	
	ReadingScheduleEntry.objects.filter(schedule = requested_schedule).delete()
	
	for i in range(0, num_entries):
		new_reading = reading_parser.parse_reading(request.POST["reading_" + str(i)])
		new_day_num = request.POST["day_num_" + str(i)]
		
		if(new_reading != None and len(new_reading) != 0 and unicode(new_day_num).isnumeric()):
			for readings in new_reading:
				for reading in reading_parser.parse_reading(readings):
					new_entry = ReadingScheduleEntry()
					new_entry.schedule = requested_schedule
					new_entry.day_num = new_day_num
					new_entry.reading = reading
					new_entry.save()
	
	messages.success(request, "Schedule successfully submited")
	return redirect("/schedule/" + str(requested_schedule.pk))
	
		
def join_schedule(request, schedule_pk):
	"""
	The logged in user will join the schedule
	"""
	requested_schedule = ReadingSchedule.objects.get(pk = schedule_pk)
	requested_schedule.signed_up.add(request.user)
	
	return redirect("/schedule/")
	
def leave_schedule(request, schedule_pk):
	"""
	The logged in user will leave the schedule
	"""
	requested_schedule = ReadingSchedule.objects.get(pk = schedule_pk)
	requested_schedule.signed_up.remove(request.user)
	
	return redirect("/schedule/")
	
def get_todays_reading(current_user):
	"""
	Returns a list containing today's reading
	"""
	schedules = []
	
	subscribed_schedules = current_user.subscribed_sched.filter()
	today = datetime.date.today()
	
	for sched in subscribed_schedules:
		readings = []
		
		day_num = (today - sched.start_date).days
		
		todays_entries = ReadingScheduleEntry.objects.filter(schedule = sched, day_num__lte = day_num + 1, day_num__gte = day_num)
		
		for entry in todays_entries:
			readings.append(entry.reading)
		
		if(today <= sched.start_date):
			schedules.append([sched.title, readings])
		
	return schedules
