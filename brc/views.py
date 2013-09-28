from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext, loader

def index(request):
	template = loader.get_template('main.html')
	context = RequestContext(request, {})
	return HttpResponse(template.render(context))
