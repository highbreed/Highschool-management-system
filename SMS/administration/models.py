from django.db import models
from django.contrib.auth.models import User

# noinspection PyUnresolvedReferences
from DB.helper_functions import Callable


# Create your models here.

class AccessLog(models.Model):
	#login = models.ForeignKey(User, on_delete=models.CASCADE)
	user_argent = models.CharField(max_length=2000, help_text="User agent. We can use this to determine operating system and browser in use.")
	date = models.DateTimeField(auto_now_add=True)
	ip = models.GenericIPAddressField(max_length=255)
	usage = models.CharField(max_length=255)

	def __str__(self):
		return str(self.login) + " " + str(self.usage) + " " + str(self.date)

	def os(self):
		try:
			#return Httpagentparser.simple_detect(self.user_argent)[0]
			return 'funck'
		except :
			return "Unknown"

	def browser(self):
		try:
			#return Httpagentparser.simple_detect(self.user_argent)[1]
			return 'Fuck'
		except:
			return "Unknown"

class Configuration(models.Model):
	name = models.CharField(max_length=100, unique=True)
	value = models.TextField(blank=True)
	file = models.FileField(blank=True, null=True, upload_to="configuration_files", help_text="Some configuration options are file uploads")
	help_text  = models.TextField(blank=True)

	def __str__(self):
		return self.name


