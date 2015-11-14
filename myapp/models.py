from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Match(models.Model):
	name=models.CharField(max_length=100)
	created_by=models.ForeignKey(User)
	is_active = models.BooleanField(default=True)
	def __unicode__(self):
		return str(self.name)



class Links(models.Model):
	link=models.CharField(max_length=500)
	match = models.ForeignKey(Match)
	team1odd=models.FloatField(default=1.0)
	team2odd=models.FloatField(default=1.0)
	time_left=models.CharField(max_length=500,null=True,blank=True)
	is_active = models.BooleanField(default=True)
	linktype = models.CharField(max_length=10, choices=(('d2l', 'dota2lounge'), ('vpd', 'vpgame dota'), ('vpp', 'vpgame p coins'), ('d2byd', 'dota 2 bestyolo dota'), ('d2byc', 'dota 2 bestyolo csgo'),('d2t', 'dota 2 top'),('nxt', 'nxtgame'),),null=True, blank=True)



	def __unicode__(self):
		return str(self.link)
