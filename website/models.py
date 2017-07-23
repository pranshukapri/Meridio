from django.db import models
from django.contrib.auth.models import Permission,User
from datetime import date
import datetime
class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	bio = models.TextField(max_length=5000,blank=True)
	location = models.CharField(max_length=100,blank=True)
	birth_date = models.DateField(null=True,blank=True)
	contrib = models.IntegerField()
	avatar = models.FileField(default='profile-icon.png')

	def __str__(self):
		return "Hello User : "+self.user.username

class SharedObjects(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	upload_obj = models.FileField()
	name = models.CharField(max_length=500)
	num_download = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	date_added = models.DateField(default = date(1997,3,30))

	def __str__(self):
		return "Object Selected : "+self.name

class Network(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	friend_pk = models.IntegerField()
	friend_name = models.CharField(max_length=500,default='')
	last_conversation = models.DateTimeField(default = datetime.datetime(1997,3,30,0,0,0,0))

	def __str__(self):
		return "User : "+self.user.username+" Friend : "+self.friend_name

class Request(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	friend_pk=models.IntegerField()
	friend_name = models.CharField(max_length=500,default='')

	def __str__(self):
		return "Users : "+self.user.username+" Target : "+self.friend_name

class Conversation(models.Model):
	network = models.ForeignKey(Network,on_delete=models.CASCADE)
	conversation = models.TextField(max_length=10000)
	conv_time = models.DateTimeField(default=datetime.datetime(1997,3,30,0,0,0,0))

	def __str__(self):
		return "Network : "+self.network.user.username+" "+self.network.friend_name
