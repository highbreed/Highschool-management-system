from django.contrib import admin
from .models import MarkingPeriod, Course, SubjectPeriod \
				, DaysOff, SchoolEvent, Period \



# Register your models here.

admin.site.register(MarkingPeriod)
admin.site.register(Course)
admin.site.register(SubjectPeriod)
admin.site.register(Period)
admin.site.register(DaysOff)

admin.site.register(SchoolEvent)
