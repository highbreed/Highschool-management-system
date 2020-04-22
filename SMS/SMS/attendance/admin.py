from django.contrib import admin
from .models import StudentAttendance, AttendanceStatus

# Register your models here.
admin.site.register(StudentAttendance)
admin.site.register(AttendanceStatus)