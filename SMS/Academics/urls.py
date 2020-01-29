from django.urls import path
from . import views


app_name = 'academic'

urlpatterns = [
	path('', views.class_management, name='class_management'),
	path('add_new_class/', views.add_class, name='add_class'),
	path('edit_class/<str:slug>/', views.edit_class_room, name='edit_classroom'),
	path('classroom/<str:slug>/', views.classroom_view, name='class_details'),
	path('streams/', views.stream_management, name='stream_management'),
	path('add_streams/', views.add_stream, name='add_stream'),
	path('edit_stream/<str:slug>/', views.edit_stream, name='edit_stream'),
	path('subjects/', views.subject_management, name='subject_management'),
	path('add_subject/', views.add_subject, name='add_subject'),
	path('edit_subject/<str:slug>/', views.edit_subject, name='edit_subject'),
	path('class_subjects/', views.class_subjects, name='class_subject' ),
	path('get_subjects/', views.get_subjects, name='get_subjects'),
	path('add_class_subject/<str:slug>/', views.add_class_subject, name='add_class_subject'),
	path('edit_class_subject/<str:slug>/', views.edit_class_subject, name='edit_class_subject'),
	path('students_attendance/', views.students_attendance_management, name='student_attendance'),

]
