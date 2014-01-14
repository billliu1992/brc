from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login

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
		return redirect('readings/')
	else:
		return redirect("/")
		
