from django.conf.urls import url
from . import views

app_name = 'student'

urlpatterns = [
	url(r'^student_details/(?P<slug>[\w-]+)/$', views.student_details, name='student_details'),
]