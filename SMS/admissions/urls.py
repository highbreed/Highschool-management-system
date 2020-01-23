from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
	url(r'^$', views.dashboard, name='dashboard'),
	url(r'^classRoom_details/(?P<slug>[\w-]+)/$', views.class_room_view, name='stream_view'),
	url(r'^students_admission/$', views.student_admission, name='student_admission'),
	path('student_details/', views.student_details, name='student_details'),
	path('teachers/', views.teachers_view, name='teachers_view'),
	path('teachers_registration/', views.teacher_admission, name='teacher_registration'),
	path('teachers_info_update/<str:slug>/',views.teacher_information_update, name='teacher_update'),
	path('teachers_details/', views.teacher_details, name="teacher_details"),
	path('delete_user/teacher/', views.teacher_delete, name='teacher_delete'),

]
