from django.contrib import admin
from .models import AccessLog, Configuration

# Register your models here.

admin.site.register(AccessLog)
admin.site.register(Configuration)