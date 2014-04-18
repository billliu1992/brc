import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from schedule.models import ReadingSchedule, ReadingScheduleEntry

from parser import date_parser, reading_parser

def all_schedules_page(request):
	"""
	Page for updating reading schedules
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		return redirect('/')
		
	#get the schedules to put on the  view
	schedules = ReadingSchedule.objects.filter(creator = request.user)
	
	schedules_text = []
	for schedule in schedules:
		schedules_text.append((schedule.title, schedule.web_friendly_title))
	
	context = RequestContext(request, {"schedules": schedules_text})
	return render_to_response('schedule/reading_schedule.html', context)
	
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
	Page for editing the schedule
	"""
	
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		return redirect('/')	#TODO change this...
		
	#get the schedule
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	
	#makes sure that it is the creator
	if(request.user != requested_schedule.creator):
		return redirect('/')	#TODO Change this...
	
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
	
	new_name = request.POST["name"]
	new_date = request.POST["start_date"]
	num_entries = int(request.POST["entries_num"])
	
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	
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
