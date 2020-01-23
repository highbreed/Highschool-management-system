from django.urls import path
from django.conf.urls import url, include
from . import views


app_name = "core"


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]
