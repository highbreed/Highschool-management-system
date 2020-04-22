from django.db import models
# noinspection PyUnresolvedReferences
from DB.models import Student

# Create your models here.

class AttendanceStatus(models.Model):
	name = models.CharField(max_length=255, unique=True,
							help_text='"Present" will not be saved but may show as a teacher option.')
	code = models.CharField(max_length=10, unique=True,
							help_text="Short code used on attendance reports. Ex: A might be the code for the name Absent")
	teacher_selectable = models.BooleanField()
	excused = models.BooleanField()
	absent = models.BooleanField(
		help_text="Some statistics need to add various types of absent statuses, such as the number in parathesis in daily attendance")
	tardy = models.BooleanField(
		help_text="Some statistics need to add various types of tardy statuses, such as the number in parathesis in daily attendance")
	half = models.BooleanField(
		help_text="Half attendance when counting. DO NOT check off absent otherwise it will double count!")

	class Meta:
		verbose_name_plural = 'Attendance Statuses'

	def __str__(self):
		return self.name

class StudentAttendance(models.Model):
	#classroom_id = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='student_attendance')
	student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_attendance')
	attendance_date = models.DateField()
	status = models.ForeignKey(AttendanceStatus, on_delete=models.PROTECT)
	notes = models.CharField(max_length=150, blank=True)
	private_notes = models.CharField(max_length=500, blank=True)
	#signed_by = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = (("student", "attendance_date", 'status'),)
		ordering = ('-attendance_date', 'student',)

	def __str__(self):
		return str(self.student)
