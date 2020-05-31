from django.urls import path
from . import views


app_name = 'academic'

urlpatterns = [
	path('', views.class_management, name='class_management'),
	path('add/new_class/', views.add_class, name='add_class'),
	path('edit/class/<str:slug>/', views.edit_class_room, name='edit_classroom'),
	path('classroom/<str:slug>/', views.classroom_view, name='class_details'),
	path('streams/', views.stream_management, name='stream_management'),
	path('add/streams/', views.add_stream, name='add_stream'),
	path('edit/stream/<str:slug>/', views.edit_stream, name='edit_stream'),
	path('subjects/', views.subject_management, name='subject_management'),
	path('add/subject/', views.add_subject, name='add_subject'),
	path('edit/subject/<str:slug>/', views.edit_subject, name='edit_subject'),
	path('class/subjects/', views.class_subjects, name='class_subject' ),
	path('get/subjects/', views.get_subjects, name='get_subjects'),
	path('add/class/subject/<str:slug>/', views.add_class_subject, name='add_class_subject'),
	path('edit/class/subject/<str:slug>/', views.edit_class_subject, name='edit_class_subject'),
	path('exam/management/', views.examination_management, name='exam_management'),
	path('add/exam/', views.add_examination, name='add_exam'),
	path('edit/exam/<str:slug>/', views.edit_examination, name='edit_exam'),


]
