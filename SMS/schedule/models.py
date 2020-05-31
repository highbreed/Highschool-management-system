from django.db import models
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

# noinspection PyUnresolvedReferences
from DB.models import AcademicYear,ClassRoom, Teacher, Student, Day, Department, Subject
# noinspection PyUnresolvedReferences
from administration.models import Configuration

# Create your models here.
class MarkingPeriod(models.Model):
	"""This is the division of school year in to semesters or Terms"""
	name = models.CharField(max_length=255)
	short_name = models.CharField(max_length=255)
	start_date = models.DateField()
	end_date = models.DateField()
	sort_order = models.IntegerField(blank=True, null=True, help_text='The order of the semester in this academic year ')
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	graded = models.BooleanField(default=False, help_text="This will allow teachers and administrators to enter final "
														  "grades for this marking period ")
	grade_posting_begins = models.DateField(blank=True, null=True)
	grade_posting_ends = models.DateField(blank=True, null=True)
	active = models.BooleanField(default=False, help_text="Teachers may only enter grades for active marking periods. "
														  "There may be more than one active marking period. ")
	show_reports = models.BooleanField(default=True, help_text="If checked this marking period will show up on reports. ")
	monday = models.BooleanField(default=True)
	tuesday = models.BooleanField(default=True)
	wednesday = models.BooleanField(default=True)
	thursday = models.BooleanField(default=True)
	friday = models.BooleanField(default=True)
	saturday = models.BooleanField(default=False)
	sunday = models.BooleanField(default=False)
	school_days = models.IntegerField(blank=True, null=True,
									  help_text="If set, this will be the number of days school is in session. "
												"If unset, the value is calculated by the days off.")

	class Meta:
		ordering = ('-start_date',)
		unique_together = (('name', 'academic_year', 'start_date', 'end_date', 'sort_order'),)

	def __str__(self):
		return self.name

	@property
	def get_school_days(self):
		school_days_list = []
		if self.monday:
			school_days_list.append('monday')
		if self.tuesday:
			school_days_list.append('tuesday')
		if self.wednesday:
			school_days_list.append('wednesday')
		if self.thursday:
			school_days_list.append('thursday')
		if self.friday:
			school_days_list.append('friday')
		if self.saturday:
			school_days_list.append('saturday')
		if self.sunday:
			school_days_list.append('sunday')
		return school_days_list



	@property
	def status(self, now_=date.today()):
		# noinspection PyTypeChecker
		if self.start_date < now_ > self.end_date:
			return 'ended'
		elif self.start_date <= now_ <= self.end_date:
			return 'active'
		elif self.start_date > now_ < self.end_date:
			return 'pending'
		elif self.active:
			return 'Active'
		else:
			return IndexError


	def clean(self):
		from django.core.exceptions import ValidationError
		# Don't allow draft entries to have pub_date.
		if self.start_date >= self.end_date:
			raise ValidationError("Cannot end before starting! ")

	def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
		super(MarkingPeriod, self).save()
		if self.active:
			# if it is marked as the active marking period then update all the tables row i the database with false
			MarkingPeriod.objects.exclude(pk=self.pk).update(active="False")


class DaysOff(models.Model):
	date = models.DateField()
	marking_period = models.ForeignKey(MarkingPeriod, on_delete=models.CASCADE)

	def __str__(self):
		return self.date

class Period(models.Model):
	name = models.CharField(max_length=255, unique=True)
	short_name = models.CharField(max_length=10, blank=True, null=True)
	sort_order = models.IntegerField()
	start_time = models.TimeField(unique=True)
	end_time = models.TimeField(unique=True)
	used_for_attendance = models.BooleanField(default=False, help_text='if marked a teacher would be able to take '
																	   'attendance for that particular period')
	ignore_for_scheduling = models.BooleanField(default=False, help_text='if checked you can avoid period clash for '
																		 ''
																		 'scheduling a student')

	class Meta:
		ordering = ('sort_order',)
		unique_together = ['name', 'start_time', 'end_time']

	def __str__(self):
		return "%s (%s-%s)" % (self.name, self.start_time.strftime('%I:%M'), self.end_time.strftime('%I:%M%p'))

	@property
	def get_table_name(self):
		return "%s - %s" % (self.start_time.strftime('%I:%M'), self.end_time.strftime('%I:%M%p'))

	def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
		if self.end_time <= self.start_time:
			raise ValueError('can not have a period where it '
							 'ends before starting....!!!Please update your time fields..')
		super(Period, self).save()


class SubjectPeriod(models.Model):
	"""Time and day for Subject meet up it can be per class or not
	NB: Holds values of  the timetable per class
	"""

	class_name = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, blank=True)
	period = models.ForeignKey(Period, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
	day_choice = (
		#ISO WEEKDAY
		('1', 'Monday'),
		('2', 'Tuesday'),
		('3', 'Wednesday'),
		('4', 'Thursday'),
		('5', 'Friday'),
		('6', 'Saturday'),
		('7', 'Sunday'),
	)
	day = models.CharField(max_length=1, choices=day_choice)
	location = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)

	def __str__(self):
		return str(self.course)

class Location(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name


class Course(models.Model):
	"""Course another name for subject"""
	active = models.BooleanField(default=True)
	full_name = models.CharField(max_length=255, unique=True)
	short_name = models.CharField(max_length=255, unique=True)
	#marking_period = models.ManyToManyField(MarkingPeriod, blank=True, help_text="the term or semester in a academic
	# year")
	#periods = models.ManyToManyField(Period, blank=True, through=CourseMeet)
	#teacher = models.ForeignKey(Teacher, blank=True, null=True, on_delete=models.SET_NULL)
	#secondary_teachers = models.ManyToManyField(Teacher, blank=True, related_name='secondary_teachers')
	graded = models.BooleanField(default=True, help_text='Teachers can submit grades for this course')
	description = models.CharField(max_length=255,blank=True)
	credits = models.DecimalField(max_length=5, max_digits=5, decimal_places=2, blank=True, null=True,
								  help_text="Credits effect gpa")
	department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
	last_grade_submission = models.DateTimeField(blank=True, null=True, editable=False)

	def __str__(self):
		return self.full_name

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		super(Course, self).save()

	@staticmethod
	def autocomplete_search_field():
		return "short_name__icontains", "full_name__icontains"

	def get_grades(self):
		for garde in self.grade_set.all():
			setattr(garde, '_course_cache', self)
			yield garde

	def is_passing(self, student, date_report=None):
		"""Is student passing course? """
		pass_score = float(Configuration.get_or_default("Passing Grade", '70').value)
		grade = self.get_final_grade(student, date_report=date_report)
		try:
			if grade >= int(pass_score):
				return True
		except :
			pass_letters = Configuration.get_or_default('Letter Passing Grade', 'A,B,C,P').value
			if grade in pass_letters.split(','):
				return True
		return False

	def get_attendance_students(self):
		"""Should be one line of code. sorry this is so awful
		Couldn't figure out any other way"""
		today , created = Day.objects.get_orc_reate(day=str(date.today().isoweekday()))
		all_ = Student.objects.filter(courseenrollment__course=self, inactive=False)
		exclude = Student.objects.filter(courseenrollment__course=self, inactive=False,
										 courseenrollment__exclude_days=today)
		ids = []
		for id in exclude.values('id'):
			ids.append(int(id['id']))
		return all_.exclude(id__in=ids)

	def get_final_grade(self, student, date_report=None):
		""" Get final grade for a course. Returns override value if available.
		date_report: optional gets grade for time period"""
			# noinspection PyUnresolvedReferences
		from grades.models import Grade
		final = Grade.objects.filter(course=self, override_final=True, student=student)
		if final.count():
			if not date_report or final[0].course.marking_period.filter(end_date__lte=date_report).count():
				final = final[0].get_grade()
		elif date_report:
			final = self.calculate_final_grade(student, date_report)
		else:
			final = self.calculate_final_grade(student)
		return final

	def calculate_final_grade(self, student, date_report=None):
		"""Calculates final grade. Does not take into account overrides.
		Note that this should math recalc_ytd_grade in gradesheet.js! """
		from SMS.grades.models import Grade
		final = Decimal(0)
		number = 0
		letter_grade = False
		grades = Grade.objects.filter(student=student, course=self)
		if date_report:
			grades = grades.filter(marking_period__end_date__lte=date_report)
		for grade in grades:
			try:
				final += grade.get_grade()
				number += 1
			# otherwise it's a letter grade.
			except TypeError:
				# I (Incomplete) results in the final grade being I
				if grade.get_grade() == "I":
					return "I"
				elif grade.get_grade() in ["P", "HP", "LP"]:
					final += 100
					number += 1
					letter_grade = True
				elif grade.get_grade() == 'F':
					number += 1
					letter_grade = True

		if number != 0:
			final = final / number
			final = Decimal(final).quantize(Decimal("0.01"), ROUND_HALF_UP)
			if letter_grade == True:
				if final > int(Configuration.get_or_default('letter_grade_required_for_pass', '60').value):
					return "P"
				else:
					return "F"
		else:
			final = None
		return final

class OmitCourseGPA(models.Model):
	"""Used to keep repeated or invalid course from affection GPA """
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)

	def __str__(self):
		return "{}{}".format(str(self.student), str(self.course))

class OmitYearGPA(models.Model):
	"""Used to keep repeated or invalid years from  affecting GPA and transcripts"""
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, help_text="Omit this year from gpa calculations "
																			   "and transcripts")

	def __str__(self):
		return "{}{}".format(str(self.student), str(self.year))


class CourseAllocation(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="name of the subject or course")
	class_allocated = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, help_text="name of the class")
	is_compulsory = models.BooleanField(default=False)
	this_academic_year = models.BooleanField(default=True, help_text="if left un checked the course will only be "
																	 "offered in this current academic period")



class Award(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class AwardStudent(models.Model):
	award = models.ForeignKey(Award, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	marking_period = models.ForeignKey(MarkingPeriod, blank=True, null=True, on_delete=models.SET_NULL)


class SchoolEvent(models.Model):
	title = models.CharField(max_length=255,
							 help_text="NB:  this is a system wide event service all events created will \n"
													   "results in system wide notification, \nFor personalised events "
													   "go to noticeboard/Events")
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	notes = models.CharField(max_length=500, blank=True, null=True)
	start = models.DateTimeField()
	end = models.DateTimeField(blank=True, null=True)

	class Meta:
		unique_together = ('title', 'academic_year')

	def __str__(self):
		return self.title
