from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ReadingEntry(models.Model):
	reading = models.CharField(max_length=50)
	date = models.DateField()
	user = models.ForeignKey(User)
		
