import datetime

from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from readings.models import ReadingEntry

from parser import date_parser, reading_parser


def readings_page(request):
	"""
	Default readings page
	"""
	#check to make sure user is logged in
	if request.user is None:
		redirect('', context)
		
	#get the readings to put on the view
	readings = ReadingEntry.objects.filter(user=request.user)
	
	readings_text = []
	for reading in readings:
		readings_text.append((reading.reading, reading.reading.replace(" ", ""), reading.date.month, reading.date.day, reading.date.year))
		
	context = RequestContext(request, {"readings": readings_text})
	return render_to_response('readings/readings.html', context)
	
def add_reading(request):
	"""
	Add a reading to the models
	"""
	#get the reading
	reading_text = request.POST["reading"]
	date_text = request.POST["date"]
	
	#parse the date
	date = date_parser.parse_date(date_text)
	if(date == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	#parse the reading
	full_reading = reading_parser.parse_reading(reading_text)
	if(full_reading == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	
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
	full_reading = reading_parser.parse_reading(reading)
	if(full_reading == None):
		return redirect("/")	#TODO Once templates are done, make this redirect/render something prettier
	
	date_obj = datetime.datetime(int(year), int(month), int(day))
	
	ReadingEntry.objects.get(date = date_obj, reading = full_reading, user = request.user).delete()
	
	return redirect('/readings/')
	
