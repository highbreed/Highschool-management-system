from grades.models import *
from rest_framework import serializers

class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Department
                fields = ('name', 'long_name',)
                
class EnrollmentStatusSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = EnrollmentStatus
                fields = ('description',)

class AssignmentTypeSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = AssignmentType
                fields = ('description',)

class CourseSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Course
                fields = ('title', 'number', 'department',)

class SemesterSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Semester
                fields = ('name', 'year',)

class SectionSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Section
                fields = ('course', 'number', 'semester',)

class AssignmentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Assignment
                fields = ('section', 'name', 'max_value', 'assign_date', 'due_date', 'assignment_type', 'a_cutoff', 'b_cutoff', 'c_cutoff', 'd_cutoff',)

class StudentSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Student
                fields = ('id', 'last_name', 'first_name', 'middle_name', 'nick_name', 'phone', 'email', 'suffix',)

class AssignmentScoreSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = AssignmentScore
                fields = ('student', 'assignment', 'score',)

class RosterSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Roster
                fields = ('section', 'student', 'enrollment_status',)

class AttendanceSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = Attendance
                fields = ('student', 'section', 'date',)

class PermissionCodeSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
                model = PermissionCode
                fields = ('permission_code', 'section', 'student',)
