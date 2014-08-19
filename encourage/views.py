import datetime
import json

from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib import messages

from readings.models import *
from encourage.models import *
from schedule.models import *

from parser.date_parser import *

def main_page(request):
	"""
	Main page for challenge
	"""
	
	all_joined_teams = request.user.joined_teams.all()
	
	challenge_status = []
	
	for team in all_joined_teams:
		schedule = team.challenge.schedule
		challenge = team.challenge
		
		result = get_consistency(request.user, schedule)
		challenge_status.append((challenge.pk, team.pk, schedule.pk, challenge.name, team.team_name, schedule.title, result["consistency"], result["completion"]))
		
	context = RequestContext(request, {"challenge_status" : challenge_status, "messages" : messages})
	return render_to_response("encourage/challenge_main.html", context)


def challenge_list(request, keywords, page_num, num_per_page):
	"""
	Page that shows all the challenges
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
	
	challenges_list = None
	
	if(keywords != None):
		challenges_list = Challenge.objects.filter(name__contains = keywords)
	else:
		challenges_list = Challenge.objects.all()
		
	challenges_list = challenges_list[(page_num-1) * num_per_page : (page_num) * num_per_page]
	
	context = RequestContext(request, {"challenges_list": challenges_list})
	return render_to_response("encourage/challenge_list.html", context)
	
def challenge_page(request, challenge_pk, sort):
	"""
	Page for a specific challenge
	"""
	
	challenge = Challenge.objects.get(pk = challenge_pk)
	
	if(challenge.invite_only and not request.user in challenge.invited):
		messages.error("You need an invite to join that Challenge. Please ask the administrator for an invite")
		return redirect("/challenge")
	
	schedule = challenge.schedule
	
	all_teams = ChallengeTeam.objects.filter(challenge = challenge)
	all_results = []
	
	for team_pos in range(len(all_teams)):
		
		team = all_teams[team_pos]
		
		team_consistency, team_completion = get_team_results(team.team_members.all(), schedule)
			
		all_results.append((team_pos, team.pk, team.team_name, team_consistency, team_completion))
		
	if(sort == "consistency"):
		all_results.sort(key=lambda item : item[2])
	else:
		all_results.sort(key=lambda item : item[3])
	
	context = RequestContext(request, {"teams" : all_results, "challenge_pk" : challenge_pk})
	return render_to_response("encourage/challenge_view.html", context)

def join_team(request, team_pk):
	"""
	Joins a challenge for the current user
	"""
	requested_team = ChallengeTeam.objects.get(pk = team_pk)
	
	if(requested_team.challenge.invite_only and not request.user in requested.team.challenge.invited):
		messages.error(request, "You need an invite to join that Challenge. Please ask the administrator for an invite")
		return redirect("/challenge")
		
	request.user.joined_teams.add(requested_team)
	messages.success(request, "You have successfully joined the team: " + requested_team.team_name)
	return redirect("/challenge/team/view/" + str(team_pk))
	
def leave_team(request, team_pk):
	requested_team = ChallengeTeam.objects.get(pk = team_pk)
	
	if(not request.user in requested_team.team_members.all()):
		messages.error(request, "You cannot leave a team that you are not in")
		return redirect("/challenge")
		
	requested_team.team_members.remove(request.user)
	
	messages.success(request, "You have successfully left the team: " + requested_team.team_name)
	return redirect("/challenge")

def view_team_page(request, team_pk):
	"""
	View the main page for a team
	"""
	
	selected_team = ChallengeTeam.objects.get(pk = team_pk)
	
	users = selected_team.team_members.all()
	
	team_name = selected_team.team_name
	
	all_results = get_team_results(users, selected_team.challenge.schedule)
	team_consistency = all_results["consistency"]
	team_completion = all_results["completion"]
	
	member_names = []
	for usr in users:
		print usr.first_name + " " + usr.last_name
		member_names.append(usr.first_name + " " + usr.last_name)
		
	join_control = "join"
	if(request.user in selected_team.team_members.all()):
		join_control = "leave"
	elif(selected_team.invite_only and not request.user in selected_team.invited.all()):
		join_control = "invite"
	
	context = RequestContext(request, { "team_pk" : team_pk, "name" : team_name, "members" : member_names, "consistency" : team_consistency, "completion" : team_completion, "join_control" : join_control, "messages" : messages })
	return render_to_response("encourage/view_team.html", context)

def create_challenge_team(request, challenge_pk):
	"""
	Creates a team for a challenge
	"""
	if request.method == "POST":
		team_name = request.POST["team-name"]
		
		new_team = ChallengeTeam()
		new_team.team_name = team_name
		
		selected_challenge = Challenge.objects.get(pk = challenge_pk)
		new_team.challenge = selected_challenge
		
		new_team.save()
		
		return redirect("/challenge/view/" + str(challenge_pk))
		
	else:
		selected_challenge = Challenge.objects.get(pk = challenge_pk)
		
		context = RequestContext(request, {"challenge_name" : selected_challenge.name})
		return render_to_response("encourage/create_team.html", context)
	
def create_challenge(request):
	"""
	Creates a challenge from form data
	"""
	if request.method == "POST":
		selected_schedule_pk = request.POST["schedule-result-selected"]
		
		selected_schedule = ReadingSchedule.objects.get(pk = selected_schedule_pk)
		
		new_challenge = Challenge()
		new_challenge.name = request.POST["challenge-name"]
		new_challenge.schedule = selected_schedule
		new_challenge.schedule_name = selected_schedule.title
		if("challenge-is-private" in request.POST):
			new_challenge.invite_only = request.POST["challenge-is-private"]
		else:
			new_challenge.invite_only = False
		new_challenge.save()
		new_challenge.admin.add(request.user)
		
		
		
		messages.success(request, "Successfully created a challenge")
		return redirect("/challenge")
		
	else:
		all_schedules = ReadingSchedule.objects.filter(start_date__gte = datetime.datetime.today())
		#turn into JSON for selector
		list_of_sched = []
		for schedule in all_schedules:
			list_of_sched.append({ 'name' : schedule.title, 'date' : parse_date_to_string(schedule.start_date), 'pk' : schedule.pk })
		
		print(json.dumps(list_of_sched))
		
		context = RequestContext(request, {"all_schedule_json" : json.dumps(list_of_sched)})
		return render_to_response("encourage/create_challenge.html", context)
	
def get_team_results(usrs, sched):
	"""
	Get the consistency and completion of an entire team
	"""	
	
	total_consistency = 0
	total_completion = 0
	for user in usrs:
		result = get_consistency(user, sched)
		
		total_consistency += result["consistency"]
		total_completion += result["completion"]
	
	team_consistency = 0
	team_completion = 0
		
	if(len(usrs) != 0):
		team_consistency = total_consistency / float(len(usrs))
		team_completion = total_completion / float(len(usrs))
		
	return { "consistency" : team_consistency, "completion" : team_completion }


def get_consistency(usr, sched):
	"""
	Get the consistency of the user for the schedule
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
	
