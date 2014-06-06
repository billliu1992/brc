from django import template

register = template.Library()

@register.filter
def get_range(value):
	"""
	Django snippet 1357
	"""
	
	return range(value)
