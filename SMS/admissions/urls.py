from django.conf.urls import url
from . import views

app_name = 'admissions'

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^stream_details/(?P<slug>[\w-]+)/$', views.class_stream_view, name='stream_view'),
	url(r'^students_admission/$', views.student_admission, name='student_admission'),
	url(r'^teachers_registration/$', views.teacher_admission, name='teacher_registration'),
	url(r'^assign_class_teacher/$', views.class_teacher, name='class_teacher_assignment'),

]
