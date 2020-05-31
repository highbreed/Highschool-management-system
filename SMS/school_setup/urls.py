from django.urls import path

from . import views

app_name = 'setup'

urlpatterns = [
	path('school/information/', views.add_school_information, name='add_school_info')
]