from django.urls import path
from . import views

app_name = 'broadcast'

urlpatterns = [
	path('broadcast/', views.broadcast_sms, name='send_sms')
]