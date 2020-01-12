from django.contrib import admin
from grades.models import *

class DepartmentAdmin(admin.ModelAdmin):
    list_display=('name','long_name')
admin.site.register(Department,DepartmentAdmin)

admin.site.register(EnrollmentStatus)
admin.site.register(AssignmentType)

class CourseAdmin(admin.ModelAdmin):
    list_display=('department','title','number')
    list_filter=['department','title','number']
admin.site.register(Course,CourseAdmin)

class SemesterAdmin(admin.ModelAdmin):
    list_display=('name','year')
    list_filter=['name','year']
admin.site.register(Semester,SemesterAdmin)

class SectionAdmin(admin.ModelAdmin):
    list_display=('number','course','semester')
    list_filter=['course','semester']
admin.site.register(Section,SectionAdmin)

class AssignmentAdmin(admin.ModelAdmin):
    list_display=('section','name','max_value','assignment_type','assign_date','due_date','a_cutoff','b_cutoff','c_cutoff','d_cutoff')
    list_filter=['section','assignment_type','name']
    search_fields=['name']
admin.site.register(Assignment,AssignmentAdmin)


class AssignmentScoreAdmin(admin.ModelAdmin):
    list_display=('assignment','student','score')
    list_filter=['assignment']
    search_fields=['student','assignment']
admin.site.register(AssignmentScore,AssignmentScoreAdmin)

class RosterAdmin(admin.ModelAdmin):
    list_display=('section','student','enrollment_status')
    list_filter=['section','enrollment_status']
    search_fields=['student']
admin.site.register(Roster,RosterAdmin)

class AttendanceAdmin(admin.ModelAdmin):
    list_display=('section','student','date')
    list_filter=['section','date']
    search_fields=['student']
admin.site.register(Attendance,AttendanceAdmin)

class PermissionCodeAdmin(admin.ModelAdmin):
    list_display=('section','permission_code','student')
    list_filter=['section']
admin.site.register(PermissionCode,PermissionCodeAdmin)
