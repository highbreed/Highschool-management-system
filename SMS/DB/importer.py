from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def generate_username(first_name, last_name):
	"""
	Generate a unique username for a **USER** based on first and last name
	Try first the first letter of the firstname plus the last name
	if fail, try adding more letters of the first name
	if fail, add an incrementing number to the end.
	This function should always find a name and never fail except in
	absurd scenarios with many users and limited varchar space
	:param first_name:
	:param last_name:
	:return:
	"""
	fname = "".join(first_name.split())
	lname = "".join(last_name.split())

	try:
		i = 1
		username = str(fname[:i]) + str(lname)
		while User.objects.filter(username=username).count() > 0:
			i + 1
			username = str(fname[:i]) + str(lname)
			if username == "": raise  ValueError("Username Error")
	except:
		number = 1
		username = str(fname[:i]) + str(lname) + str(number)
		while User.objects.filter(username=username).count() > 0:
			number += 1
			username = str(fname[:i]) + str(lname) + str(number)
	return str.lower(username)

def mail_agent(recipient_list, subject, message):
	email_from = settings.EMAIL_HOST_USER
	if len(recipient_list) > 1:
		for recipient in recipient_list:
			send_mail(subject, message, email_from, recipient)
	else:
		send_mail(subject, message, email_from, recipient_list)
	return 'success'