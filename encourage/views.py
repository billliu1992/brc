import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from readings.models import *
from schedule.models import *

def get_reading_schedule_consistency(request):
	"""
	Get the consistency of all the reading schedules
	"""
	
	signed_up_schedules = request.user.subscribed_sched.all()
	
	schedule_status = {}
	schedule_consistency = {}
	schedule_completion = {}
	for sched in signed_up_schedules:
		reading_day_num = datetime.date.today() - sched.start_date
		schedule_entries = ReadingScheduleEntry.objects.filter(schedule = sched, day_num__lte = reading_day_num.days + 1)
		readings = ReadingEntry.objects.filter(date__gte = sched.start_date, user = request.user)
		
		day_num_status = {}
		consistency = 0
		completion = 0
		total_num_entries = 0
				
		for entry in schedule_entries:
			reading_status = 0	#0 - not read, 1 - read but late, 2 - read and on time
			for reading in readings:
				if(reading.reading == entry.reading):
					#decide whether or not a reading was finished, late, or on time
					reading_deadline = sched.start_date + datetime.timedelta(entry.day_num)
				
					if(reading.date <= reading_deadline):
						reading_status = 2
						consistency += 1
						completion += 1
					elif(reading.date > reading_deadline and reading_status == 0):	#do not want to change an entry that was on time to late if the reading reads a reading twice
						reading_status = 1
						completion += 1
						
					total_num_entries += 1
			
			if(total_num_entries > 0):
				consistency = float(consistency) / total_num_entries
				completion = float(completion) / total_num_entries
			else:
				consistency = 0
				completion = 0
			
			if(not entry.day_num in day_num_status):
				day_num_status[entry.day_num] = {}
			day_num_status[entry.day_num][entry.reading] = reading_status
			
		schedule_status[sched.title] = day_num_status
		schedule_consistency[sched.title] = consistency
		schedule_completion[sched.title] = completion
		
	context = RequestContext(request, {"schedule_status" : schedule_status, "schedule_consistency" : schedule_consistency, "schedule_completion" : schedule_completion})
	return render_to_response("encourage/encourage_main.html", context)
	
