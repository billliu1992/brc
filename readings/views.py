import datetime
import calendar

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from readings.models import ReadingEntry

from parser_util import date_parser, reading_parser, percent_parser

def readings_page(request):
	"""
	Used for debug, not used anymore
	
	Default readings page
	"""
	#check to make sure user is logged in
	if(not request.user.is_authenticated()):
		return redirect('/')
		
	#get the readings to put on the view
	today = datetime.date.today()
	#readings = ReadingEntry.objects.filter(user=request.user, date__lte=today, date__gte=(today - datetime.timedelta(30))).order_by("-date")
	readings = ReadingEntry.objects.filter(user=request.user).order_by("-date")
	num_month = len(readings)
	readings = readings[:15]
	
	readings_text = []
	for reading in readings:
		readings_text.append((reading.pk, reading.reading, reading.reading.replace(" ", ""), reading.date.month, reading.date.day, reading.date.year))
	
	consistency_month = percent_parser.parse_percent(get_consistency_month(request.user), True)
	consistency_week = percent_parser.parse_percent(get_consistency_week(request.user), True)
	
	context = RequestContext(request, {"readings": readings_text, "consistency_month": consistency_month, "consistency_week": consistency_week, "num_month":num_month,  "messages": messages})
	return render_to_response('readings/readings.html', context)
	
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
		messages.error(request, "Incorrect date format!")
		return redirect("/readings/")
	#parse the reading
	full_readings = reading_parser.parse_reading(reading_text)
	if(full_readings == None):
		messages.error(request, "Incorrect verse format!")
		return redirect("/readings/")
		
	today = datetime.datetime.today()
	if(today < date):
		messages.error(request, "Please enter a date before today")
		return redirect("/readings/") 
	
	for full_reading in full_readings:
		reading = ReadingEntry()
		reading.user = request.user
		reading.reading = full_reading
		reading.date = date
		reading.save()
	
	messages.success(request, "Successfully entered a reading!")
	return redirect('/readings/')
	
def delete_reading(request, reading_pk):
	"""
	Delete the reading at date for the current user
	"""
	if(request.method == "GET"):
		redirect('/readings')
	
	try:
		ReadingEntry.objects.get(pk = reading_pk).delete()
	except e:
		messages.error(request, "Error deleting reading")
		return redirect("/readings")
	
	messages.success(request, "Reading successfully deleted")
	return redirect('/readings')
	
def get_consistency_month(current_user):
	"""
	Gets how consistent a user is
	Returns the consistency between 0 to 1
	"""
	days_read_month = 0
	today = datetime.date.today()
	number_of_days = calendar.monthrange(today.year, today.month)[1]	#get number of days in month
	
	for dayNum in range(0, 30):
		if(len(ReadingEntry.objects.filter(user = current_user, date = (today - datetime.timedelta(dayNum)))) != 0):
			days_read_month += 1
	
	return days_read_month / float(number_of_days)
	
def get_consistency_week(current_user):
	"""
	Gets how consistent a user is
	Returns the consistency between 0 to 1
	"""
	days_read_week = 0
	today = datetime.date.today()
	
	for dayNum in range(0, 7):
		if(len(ReadingEntry.objects.filter(user = current_user, date = today - datetime.timedelta(dayNum))) != 0):
			days_read_week += 1
	
	return days_read_week / 7.0
	

	
