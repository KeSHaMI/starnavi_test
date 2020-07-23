from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
	email = models.EmailField(max_length=255, unique=True)
	last_action_time = models.DateTimeField(blank=True, null=True) 
	REQUIRED_FIELDS = ['password', 'username']

	USERNAME_FIELD = 'email'

	def __str__(self):
		return self.username



class Post(models.Model):
	#I'm not sure if cascade is a proper action, but as it isn't mentioned I've decided to make it as usual
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
	title = models.CharField(max_length=200, blank=True)
	body = models.TextField(blank=True)
	date_created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return self.title


class Like(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)


	def __str__(self):
		return f'{self.post.title} liked by {self.user.username}'

