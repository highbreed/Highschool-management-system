from django.conf.urls import url
from . import views


app_name = 'academic'

urlpatterns = [
	url(r'^$', views.class_management, name='class_management'),
	url(r'^add_streams/$', views.add_stream, name='add_stream'),
	url(r'^link_class_stream/$', views.link_class_stream, name='class_stream'),
	url(r'^add_new_class/$', views.add_class, name='add_class'),
	url(r'^add_subjects/$', views.add_subjects, name='add_subjects'),

]
