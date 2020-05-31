from django.contrib import admin
from .models import Grade,GradeComment

# Register your models here.

admin.site.register(GradeComment)
admin.site.register(Grade)
