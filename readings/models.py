from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ReadingEntry(models.Model):
	reading = models.CharField()
	date = models.DateField()
	user = models.ForeignKey(User)
	
class ReadingScheduleEntry(models.Model):
	reading = models.CharField()
	startDate = models.DateField()
	endDate = models.DateField()
	
	
