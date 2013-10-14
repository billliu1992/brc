from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ReadingEntry(models.Model):
	reading = models.CharField(max_length=50)
	date = models.DateField()
	user = models.ForeignKey(User)
	
class ReadingSchedule(models.Model):
	title = models.CharField(max_length=100)
	web_friendly_title = models.CharField(max_length=100)
	creator = models.ForeignKey(User, related_name = "created_sched")
	signed_up = models.ManyToManyField(User, related_name = "subscribed_sched")
	
class ReadingScheduleEntry(models.Model):
	reading = models.CharField(max_length=50)
	readDate = models.DateField()
	schedule = models.ForeignKey(ReadingSchedule)
	#class Meta:
	#	order_with_respect_to = 'readDate'
		
