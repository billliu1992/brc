import datetime

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from readings.models import *
from encourage.models import *
from schedule.models import *

def main_page(request):
	"""
	Main page for challenge
	"""
	
	all_joined_teams = request.user.joined_teams.all()
	
	challenge_status = []
	
	for team in all_joined_teams:
		schedule = team.challenge.schedule
		
		result = get_consistency(request.user, schedule)
		challenge_status.append((schedule.pk, schedule.name, result["consistency"], result["completion"]))
		
	context = RequestContext(request, {"challenge_status" : challenge_status, "messages" : messages})
	return render_to_response("encourage/encourage_main.html", context)
	
def challenge_page(request, challenge_pk):
	"""
	Page for a specific challenge
	"""
	
	challenge = Challenge.objects.get(pk = challenge_pk)
	
	if(challenge.invite_only and not request.user in challenge.invited):
		messages.error("You need an invite to join that Challenge. Please ask the administrator for an invite")
		return redirect("/encourage")
	
	schedule = challenge.schedule
	
	all_teams = challenge.joined_teams.all()
	all_results = []
	for team in all_teams:
		
		total_consistency = 0
		total_completion = 0
		
		for user in team.team_members:
			result = get_consistency(user, schedule)
			
			total_consistency += result["consistency"]
			total_completion += result["completion"]
			
		all_results.append((team.pk, team.team_name, total_consistency / float(team.team_members), total_completion / float(team.team_members)))
		
	all_results.sort(key=lambda item : item[2])
	
	context = RequestContext(request, {"all_results" : all_results})
	return render_to_response("encourage/encourage_main.html", context)

def join_team(request, challenge_pk, team_pk):
	"""
	Joins a challenge for the current user
	"""
	if(challenge.invite_only and not request.user in challenge.invited):
		messages.error("You need an invite to join that Challenge. Please ask the administrator for an invite")
		return redirect("/encourage")
		
	request.user.joined_teams.add(ChallengeTeam.objects.get(pk = team_pk))
	
def create_challenge(request):
	"""
	Creates a team from form data
	"""
	pass

def get_consistency(usr, sched):
	"""
	Get the consistency of the user for the current schedule
	"""

	reading_day_num = datetime.date.today() - sched.start_date
	schedule_entries = ReadingScheduleEntry.objects.filter(schedule = sched, day_num__lte = reading_day_num.days + 1)
	readings = ReadingEntry.objects.filter(date__gte = sched.start_date, user = usr)
	
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
		
	return {'consistency': consistency, 'completion': completion}
	
def get_reading_schedule_consistency(request):
	"""
	Deprecated?
	
	Get the consistency of all the reading schedules for the current signed in user
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
	
