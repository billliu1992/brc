from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ReadingEntry(models.Model):
	reading = models.CharField(max_length=50)
	date = models.DateField()
	user = models.ForeignKey(User)
	
class ReadingSchedule(models.Model):
	title = models.CharField(max_length=100)
	
class ReadingScheduleEntry(models.Model):
	reading = models.CharField(max_length=50)
	readDate = models.DateField()
	schedule = models.ForeignKey(ReadingSchedule)
	
