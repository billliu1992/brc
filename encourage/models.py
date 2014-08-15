from django.db import models
from django.contrib.auth.models import User

from schedule.models import ReadingSchedule

# Create your models here.
class Challenge(models.Model):
	name = models.CharField(max_length = 50, unique=True)
	schedule_name = models.CharField(max_length = 50)
	schedule = models.ForeignKey(ReadingSchedule)
	invite_only = models.BooleanField()
	admin = models.ManyToManyField(User, related_name = "admin_of")
	invited = models.ManyToManyField(User, related_name = "invitations")

class ChallengeTeam(models.Model):
	team_name = models.CharField(max_length = 50)
	team_members = models.ManyToManyField(User, related_name = "joined_teams")
	challenge = models.ForeignKey(Challenge)

