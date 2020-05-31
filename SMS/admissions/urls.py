from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('classRoom/details/<str:slug>/', views.class_room_view, name='stream_view'),
	path('teachers/', views.teachers_view, name='teachers_view'),
	path('teachers/registration/', views.teacher_admission, name='teacher_registration'),
	path('teachers/info/update/<str:slug>/',views.teacher_information_update, name='teacher_update'),
	path('teachers/details/', views.teacher_details, name="teacher_details"),
	path('delete/user/teacher/', views.teacher_delete, name='teacher_delete'),
	path('parents/', views.parent_list, name='parents_view'),
	path('parents/details/', views.parents_details, name='parent_details'),
	path('parents/update/<str:slug>/',views.parent_update, name='parent_edit'),
	path('students/admission/', views.student_admission, name='student_admission'),
	path('student/details/', views.student_details, name='student_details'),
	path('students/view/', views.student_view, name='students_view'),
	path('students/update/<str:slug>/', views.student_update, name='student_edit'),


]
