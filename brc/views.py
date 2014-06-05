from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib import messages

from readings.views import get_consistency_week, get_consistency_month
from schedule.views import get_todays_reading

def index(request):
	"""
	Index
	For the index page
	"""
	#go to readings page if logged in
	#if(request.user.is_authenticated()):
	#	return redirect('readings/')
	
	context = RequestContext(request, {})
	return render_to_response('front.html', context)
	
def authenticate_login(request):
	"""
	Login
	Grabs the user details from the login page and logs in
	"""
	#get the username and password
	usernam = request.POST["username"]
	passwor = request.POST["password"]
	
	user = authenticate(username=usernam, password = passwor)
	
	if user is not None:
		login(request, user)
		context = RequestContext(request, {})
		return redirect('/profile')
	else:
		return redirect("/")
		
def profile_page(request):
	"""
	Profile
	Shows a summary of the profile, first page that you hit after logging in
	"""
	if(not request.user.is_authenticated()):
		return redirect("/")
	
	#pass basic information
	user_name = request.user.username
	consistency_month = get_consistency_month(request.user)
	consistency_week = get_consistency_week(request.user)
	todays_reading = get_todays_reading(request.user)
	
	context = RequestContext(request, {"user_name" : user_name, "consistency_month" : consistency_month, "consistency_week" : consistency_week, "todays_reading": todays_reading, "messages": messages})
	return render_to_response('profile.html', context)
		
