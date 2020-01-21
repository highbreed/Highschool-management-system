from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^classRoom_details/(?P<slug>[\w-]+)/$', views.class_room_view, name='stream_view'),
	url(r'^students_admission/$', views.student_admission, name='student_admission'),
	url(r'^teachers_registration/$', views.teacher_admission, name='teacher_registration'),
	path('student_details/', views.student_details, name='student_details'),

]
