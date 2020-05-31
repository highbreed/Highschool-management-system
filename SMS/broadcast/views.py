from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from twilio.rest import Client



def broadcast_sms(request):
	recipients = [
		"+254795112229",
	]
	message_to_broadcast = "hey stephen this is a fucking test my brother"
	client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

	for recipient in recipients:
		if recipient:
			client.messages.create(to=recipient,
								   from_=settings.TWILIO_NUMBER,
								   body=message_to_broadcast)
	return HttpResponse("message sent!", 200)