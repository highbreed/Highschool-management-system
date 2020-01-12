from django.conf.urls import url

from . import views

app_name = 'grades'

urlpatterns = [
    # ex: /grades/
    url(r'^$', views.section_index, name='section_index'),
    # ex: /grades/5/
    url(r'^(?P<section_id>\d+)/$', views.section, name='section'),
    # ex: /grades/5/roster/
    url(r'^(?P<section_id>\d+)/roster/$', views.roster, name='roster'),
    # ex: /grades/5/assignmets/
    url(r'^(?P<section_id>\d+)/assignments/$', views.assignments, name='assignments'),
    # ex: /grades/5/assignmets/
    url(r'^(?P<section_id>\d+)/assignments/(?P<assignment_id>\d+)$', views.assignment, name='assignment'),
    # ex: /grades/5/students/1234/
    url(r'^(?P<section_id>\d+)/roster/(?P<student_id>\d+)/$', views.roster_student, name='roster_student'),
    # ex: /grades/5/hw_entry/
    url(r'^(?P<section_id>\d+)/hw_entry/$', views.hw_entry, name='hw_entry'),
    # ex: /grades/5/view_scores/
    url(r'^(?P<section_id>\d+)/view_scores/$', views.view_scores, name='view_scores'),
    # Webservice to add/remove homework scores. For use by the hw_entry page above.
    url(r'^(?P<section_id>\d+)/hw_entry/(?P<student_id>\d+)/(?P<assignment_id>\d+)/$', views.hw_assignment_add_remove, name='hw_entry_add_remove'),
]
