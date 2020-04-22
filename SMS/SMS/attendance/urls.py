from django.urls import path

from . import views

app_name = 'attendance'

urlpatterns = [
	path('student/attendance/', views.student_attendance_manager, name='students_attendance'),
	path('student/attendance/register/', views.student_attendance_register, name='student_attendance_register'),
	path('student/attendance/report/', views.student_attendance_report, name='students_attendance_report'),
	path('test/', views.teacher_attendance)
]