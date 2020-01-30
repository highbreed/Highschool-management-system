from django.urls import path
from . import views

app_name = 'admissions'

urlpatterns = [
	path('', views.dashboard, name='dashboard'),
	path('classRoom_details/<str:slug>/', views.class_room_view, name='stream_view'),
	path('teachers/', views.teachers_view, name='teachers_view'),
	path('teachers_registration/', views.teacher_admission, name='teacher_registration'),
	path('teachers_info_update/<str:slug>/',views.teacher_information_update, name='teacher_update'),
	path('teachers_details/', views.teacher_details, name="teacher_details"),
	path('delete_user/teacher/', views.teacher_delete, name='teacher_delete'),
	path('parents/', views.parent_list, name='parents_view'),
	path('parents_details/', views.parents_details, name='parent_details'),
	path('parents_update/<str:slug>/',views.parent_update, name='parent_edit'),
	path('students_admission/', views.student_admission, name='student_admission'),
	path('student_details/', views.student_details, name='student_details'),
	path('students_view/', views.student_view, name='students_view'),
	path('students_update/<str:slug>/', views.student_update, name='student_edit'),


]
