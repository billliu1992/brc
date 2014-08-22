from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

from readings.views import get_consistency_week, get_consistency_month
from schedule.views import get_todays_reading

def index(request, error_message):
	"""
	Index
	For the index page
	"""
	#go to readings page if logged in
	#if(request.user.is_authenticated()):
	#	return redirect('readings/')
	
	if(request.user.is_authenticated()):
		return redirect("/profile")
	
	popup_id = None
	full_message = None
	if("err" in request.GET):
		if(request.GET["err"] == "pwnomatch"):
			popup_id = "register-box"
			full_message = "Your passwords did not match"
		elif(request.GET["err"] == "emailexists"):
			popup_id = "register-box"
			full_message = "That e-mail already exists"
		elif(request.GET["err"] == "wrongcred"):
			popup_id = "login-box"
			full_message = "Your e-mail and/or password is incorrect"
	
	context = RequestContext(request, {"popup_id" : popup_id, "message" : full_message})
	return render_to_response('front.html', context)
	
def new_user_register(request):
	"""
	Registers a new user
	"""
	first_name = request.POST["first-name"]
	last_name = request.POST["last-name"]
	email = request.POST["email"]
	password1 = request.POST["password1"]
	password2 = request.POST["password2"]
	
	if(len(User.objects.filter(email = email)) > 0):
		return redirect("/?err=emailexists")
	
	if(password1 != password2):
		return redirect("/?err=pwnomatch")
	
	new_user = User.objects.create_user(email, email, password1)
	new_user.first_name = first_name
	new_user.last_name = last_name
	new_user.save()

	login(request, new_user)
	return redirect("/profile")
	
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
		return redirect("/?err=wrongcred")

def logout_request(request):
	"""
	Logout
	"""
	logout(request)
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
		
