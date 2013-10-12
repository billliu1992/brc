from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from readings.models import ReadingEntry

from parser import date_parser

def readings_page(request):
	"""
	readings_page
	Default readings page
	"""
	#check to make sure user is logged in
	if request.user is None:
		redirect('', context)
		
	#get the readings to put on the view
	readings = ReadingEntry.objects.filter(user=request.user)
	
	readings_text = []
	for reading in readings:
		readings_text.append((reading.reading, str(reading.date)))
		
	context = RequestContext(request, {"readings": readings_text})
	return render_to_response('readings/readings.html', context)
	
def add_reading(request):
	"""
	add_reading
	Add a reading to the models
	"""
	
	#get the reading
	reading_text = request.POST["reading"]
	date_text = request.POST["date"]
	
	#parse the date
	date = date_parser.parse_date(date_text)
	if(date == None):
		return redirect("/")
	
	reading = ReadingEntry()
	reading.user = request.user
	reading.reading = reading_text
	reading.date = date
	reading.save()
	
	return redirect('/readings/')
