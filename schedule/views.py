import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from schedule.models import ReadingSchedule, ReadingScheduleEntry
from readings.models import *

from parser import date_parser, reading_parser

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
		created_schedules_text.append((schedule.title, schedule.web_friendly_title))
	
	#get the subscribed schedules	
	subscribed_schedules = request.user.subscribed_sched.all()
	
	print(subscribed_schedules)
	
	subscribed_schedules_text = []
	for schedule in subscribed_schedules:
		subscribed_schedules_text.append((schedule.title, schedule.web_friendly_title))
	
	context = RequestContext(request, {"created_schedules": created_schedules_text, "subscribed_schedules": subscribed_schedules_text, "messages": messages})
	return render_to_response('schedule/schedule_main.html', context)
	
def new_schedule(request):
	"""
	Create a new schedule with information from your post data
	"""
	new_schedule_name = request.POST["schedule_name"]
	#start_date_str = request.POST["start_date"]
	#start_date = date_parser.parse_date(start_date_str)
	
	#check to make sure that the name is not taken
	if(len(ReadingSchedule.objects.filter(title = new_schedule_name)) != 0):
		return redirect('/')	#TODO Change this to something better once templates are done
	if(new_schedule_name.replace(" ", "").isalnum() == False):
		return redirect('/')	#TODO Change this to something better once templates are done
	if(len(new_schedule_name) == 0):
		return redirect('/')	#TODO Change this to something better once templates are done
	#if(start_date == None):
	#	return redirect('/')
	
	new_schedule = ReadingSchedule()
	new_schedule.title = new_schedule_name
	new_schedule.web_friendly_title = new_schedule_name.replace(" ", "")
	new_schedule.creator = request.user
	new_schedule.start_date = datetime.date.today()
	new_schedule.save()
	
	return redirect("/schedule/")
	
def view_schedule_page(request, schedule):
	"""
	Page for viewing the schedule
	
	The code for the view splits the schedule into 4 (uneven) columns
	"""
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	readings = ReadingEntry.objects.filter(date__gte = requested_schedule.start_date, user = request.user)
	
	subscribed = requested_schedule in request.user.subscribed_sched.all()
	
	num_cols = 4
	
	#get the readings to put on the view
	schedule_entries = ReadingScheduleEntry.objects.filter(schedule = requested_schedule)
	
	column_length = len(schedule_entries) / num_cols + 1
	entry_text = []
	for i in range(num_cols):
		entry_text.append([])
	
	
	startdate = requested_schedule.start_date
	for i in range(len(schedule_entries)):
		deadline_date = startdate + datetime.timedelta(days = schedule_entries[i].day_num)

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
	
	context = RequestContext(request, {"title":requested_schedule.title, "all_entries": entry_text})

	return render_to_response('schedule/view_schedule.html', context)
	
	
def edit_schedule_page(request, schedule):
	"""
	Page for editing the schedule
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		messages.error(request, "Log in to edit this schedule!")
		return redirect('/')
		
	#get the schedule
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	
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
	
def delete_schedule(request, schedule):
	"""
	Delete the schedule
	Will (probably) not delete the schedule from memory, just orphan the schedule
	and allow someone else to take it over
	"""
	return redirect("/schedules/")
	
def submit_schedule(request, schedule):
	"""
	Submit modifications to a schedule
	"""
	
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		messages.error(request, "Log in to edit this schedule!")
		return redirect('/')
	
	new_name = request.POST["name"]
	new_date = request.POST["start_date"]
	num_entries = int(request.POST["entries_num"])
	
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	
	#makes sure that it is the creator
	if(request.user != requested_schedule.creator):
		messages.error(request, "You do not have permission to edit this schedule!")
		return redirect('/schedules/')
	
	requested_schedule.title = new_name
	requested_schedule.web_friendly_title = new_name.replace(" ", "")
	
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
	
	return redirect("/schedule/" + new_name.replace(" ", ""))
	
		
def join_schedule(request, schedule):
	"""
	The logged in user will join the schedule
	"""
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	requested_schedule.signed_up.add(request.user)
	
	return redirect("/schedule/")
	
def leave_schedule(request, schedule):
	"""
	The logged in user will leave the schedule
	"""
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	requested_schedule.signed_up.remove(request.user)
	
	return redirect("/schedule/")
	
def get_todays_reading(current_user):
	"""
	Returns a list containing today's reading
	"""
	schedules = []
	
	subscribed_schedules = current_user.subscribed_sched.all()
	today = datetime.date.today()
	
	for sched in subscribed_schedules:
		readings = []
		
		day_num = (today - sched.start_date).days
		
		todays_entries = ReadingScheduleEntry.objects.filter(schedule = sched, day_num__lte = day_num + 1, day_num__gte = day_num)
		
		for entry in todays_entries:
			readings.append(entry.reading)
			
		schedules.append([sched.title, readings])
		
		print schedules
		
	return schedules
