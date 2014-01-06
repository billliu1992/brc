from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ReadingSchedule(models.Model):
	title = models.CharField(max_length=100)
	web_friendly_title = models.CharField(max_length=100)
	creator = models.ForeignKey(User, related_name = "created_sched")
	signed_up = models.ManyToManyField(User, related_name = "subscribed_sched")
	start_date = models.DateField()
	
class ReadingScheduleEntry(models.Model):
	reading = models.CharField(max_length=50)
	day_num = models.IntegerField()
	schedule = models.ForeignKey(ReadingSchedule)
	#class Meta:
	#	order_with_respect_to = 'readDate'
