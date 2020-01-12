from django.contrib import admin
from .models import *
from DB.models import *
# Register your models here.

admin.site.register(Address)
admin.site.register(Teacher)
admin.site.register(SubjectAllocation)
admin.site.register(ClassTeachers)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(StudentClass)
admin.site.register(AcademicYear)
admin.site.register(Term)
admin.site.register(CarryOverStudent)
admin.site.register(RepeatingStudent)
admin.site.register(Result)
admin.site.register(SchoolEvent)