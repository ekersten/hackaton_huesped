from django.db import models
from django.conf import settings

# Create your models here.
class Client (models.Model):
	name = models.CharField(max_length=200)
	cpi = models.DecimalField(max_digits=7, decimal_places=4)
	cpc = models.DecimalField(max_digits=7, decimal_places=4)
	logo = models.ImageField(upload_to='clients')
	url = models.URLField()

class Impression(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	client = models.ForeignKey('Client')
	user = models.ForeignKey(settings.AUTH_USER_MODEL)

class Click(models.Model):
	timestamp = models.DateTimeField(auto_now_add=True)
	client = models.ForeignKey('Client')
	user = models.ForeignKey(settings.AUTH_USER_MODEL)	

class Signature(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	line1 = models.TextField(blank=True, null=True)
	line2 = models.TextField(blank=True, null=True)
	line3 = models.TextField(blank=True, null=True)
	line4 = models.TextField(blank=True, null=True)