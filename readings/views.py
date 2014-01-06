import datetime
import calendar

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from readings.models import ReadingEntry

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

	
