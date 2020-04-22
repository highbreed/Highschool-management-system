from django.urls import path

from . import views
from .timetabler import views as tabler_view

app_name = 'schedule'

urlpatterns = [
	path('', views.schedule_dashboard, name='dashboard'),
	path('add_academic_year/', views.add_academic_year, name='academic_year_setup'),
	path('school/calender/', views.school_calender, name='school_calender'),
	path('add/school/events/', views.add_events, name='add_event'),
	path('get/school/events/', views.get_events, name='get_events'),
	path('marking/periods/', views.marking_period_dsh, name='marking_period_dsh'),
	path('add/marking/periods/', views.add_marking_period, name='add_marking_period'),
	path('school/periods/', views.add_periods, name='school_periods'),
	path('school/info/', views.get_school_information, name='school_info'),
	path('add/school/info/', views.add_school_information, name='add_school_info'),
	path('create/timetable/', tabler_view.create_timetable_view, name='create_timetable' ),
	path('manage/timetable/', tabler_view.timetable_manager_view, name='manage_timetable' ),
]