import datetime
import calendar

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from readings.models import ReadingEntry, ReadingSchedule, ReadingScheduleEntry

from parser import date_parser, reading_parser, percent_parser


def readings_page(request):
	"""
	Default readings page
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		return redirect('/')
		
	#get the readings to put on the view
	readings = ReadingEntry.objects.filter(user=request.user)
	
	readings_text = []
	for reading in readings:
		readings_text.append((reading.reading, reading.reading.replace(" ", ""), reading.date.month, reading.date.day, reading.date.year))
	
	consistency = percent_parser.parse_percent(get_consistency(request.user), True)
	
	context = RequestContext(request, {"readings": readings_text, "consistency": consistency})
	return render_to_response('readings/readings.html', context)
	
def readings_schedule_page(request):
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
	return render_to_response('readings/reading_schedule.html', context)
	
def new_schedule(request):
	"""
	Create a new schedule with information from your post data
	"""
	new_schedule_name = request.POST["schedule_name"]
	
	#check to make sure that the name is not taken
	if(len(ReadingSchedule.objects.filter(title = new_schedule_name)) != 0):
		return redirect('/')	#TODO Change this to something better once templates are done
	if(new_schedule_name.replace(" ", "").isalnum() == False):
		return redirect('/')	#TODO Change this to something better once templates are done
	if(len(new_schedule_name) == 0):
		return redirect('/')	#TODO Change this to something better once templates are done
	
	new_schedule = ReadingSchedule()
	new_schedule.title = new_schedule_name
	new_schedule.web_friendly_title = new_schedule_name.replace(" ", "")
	new_schedule.creator = request.user
	new_schedule.start_date = datetime.date.today()
	new_schedule.save()
	
	return redirect("/readings/schedules/")
	
def edit_schedule_page(request, schedule):
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
	for entry in schedule_entries:
		entry_text.append((entry.reading, entry.day_num))
	
	context = RequestContext(request, {"title":requested_schedule.title, "entries":entry_text, "entries_length":range(0,len(entry_text))})
	return render_to_response('readings/edit_reading_schedule.html', context)
	
def delete_schedule(request, schedule):
	"""
	Delete the schedule
	Will (probably) not delete the schedule from memory, just orphan the schedule
	and allow someone else to take it over
	"""
	
	return redirect("/readings/schedules/")
	
def submit_schedule(request, schedule):
	"""
	Submit modifications to a schedule
	"""
	
	num_entries = int(request.POST["total_num_entries"])	#TODO FIX ME AFTER DONE DEBUGGING
	
	requested_schedule = ReadingSchedule.objects.get(web_friendly_title = schedule)
	
	ReadingScheduleEntry.objects.filter(schedule = requested_schedule).delete()
	
	for i in range(0, num_entries+1):
		new_reading = reading_parser.parse_reading(request.POST["reading_" + str(i)])
		new_day_num = request.POST["day_num_" + str(i)]
		
		if(new_reading != None and len(new_reading) != 0 and new_day_num.isnumeric()):
			for reading in new_reading:
				new_entry = ReadingScheduleEntry()
				new_entry.schedule = requested_schedule
				new_entry.day_num = new_day_num
				new_entry.reading = reading
				new_entry.save()
	
	return redirect("/readings/schedules/" + schedule)
	
def add_schedule_reading(request):
	"""
	Adds an entry to the reading schedule
	"""
	
	#get the reading
	reading_text = request.POST["reading"]
	date_text = request.POST["date"]
	
	#parse the reading
	full_readings = reading_parser.parse_reading(reading_text)
	if(full_readings == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	
	for full_reading in full_readings:
		reading = ReadingScheduleEntry()
		reading.user = request.user
		reading.reading = full_reading
		reading.day_num = date
		reading.save()
	
	return redirect('/readings/schedules/')
	
def add_reading(request):
	"""
	Add a reading to the models
	"""
	if(request.method == "GET"):
		redirect('/readings')

	#get the reading
	reading_text = request.POST["reading"]
	date_text = request.POST["date"]
	
	#parse the date
	date = date_parser.parse_date(date_text)
	if(date == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	#parse the reading
	full_readings = reading_parser.parse_reading(reading_text)
	if(full_readings == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	
	for full_reading in full_readings:
		reading = ReadingEntry()
		reading.user = request.user
		reading.reading = full_reading
		reading.date = date
		reading.save()
	
	return redirect('/readings/')
	
def delete_reading(request, reading, month, day, year):
	"""
	Delete the reading at date for the current user
	"""
	if(request.method == "GET"):
		redirect('/readings')
	
	full_reading = reading_parser.parse_reading(reading)
	if(full_reading == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	
	date_obj = datetime.datetime(int(year), int(month), int(day))
	
	ReadingEntry.objects.get(date = date_obj, reading = full_reading[0], user = request.user).delete()
	
	return redirect('/readings/')
	
def get_consistency(current_user):
	"""
	Gets how consistent a user is
	Returns the consistency between 0 to 1
	"""
	days_read_month = 0
	today = datetime.date.today()
	number_of_days = calendar.monthrange(today.year, today.month)[1]	#get number of days in month
	
	for day in calendar.Calendar(0).itermonthdates(today.year, today.month):
		if(len(ReadingEntry.objects.filter(user = current_user, date = day)) != 0):
			days_read_month += 1
	
	return days_read_month / float(number_of_days)
		
	
