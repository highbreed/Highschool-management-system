from django.urls import path

from . import  views

app_name = 'noticeboard'

urlpatterns = [
	path('', views.notification_manager, name='notification_manager'),
	path('add/notification/', views.add_notification, name='add_notification'),
	path('edit/notification/<slug:notice_id>/', views.edit_notification, name='edit_notification'),
]