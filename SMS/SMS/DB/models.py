import os
from datetime import datetime, date

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import Group, User
from django.utils import timezone

from django_countries.fields import CountryField



from .validators import subject_validator, stream_validator, students_date_of_birth_validator
from .scripts import assign_admission_numbers
from .common_objs import *
# noinspection PyUnresolvedReferences
from administration.models import Configuration


class DepartmentGraduationCredits(models.Model):
	department = models.ForeignKey('Department', on_delete=models.CASCADE)
	class_year = models.ForeignKey('AcademicYear', on_delete=models.CASCADE, help_text='Also applies to subsequent years '
																					 'unless a more recent requirement'
																					 ' exists.')
	credits = models.DecimalField(max_digits=5, decimal_places=2, unique=True)

	class Meta:
		unique_together = ('department', 'credits')




class Department(models.Model):
	name = models.CharField(max_length=255, unique=True)
	order_rank = models.IntegerField(blank=True, null=True, help_text="Rank that courses will show up in reports")

	def get_graduation_credits(self, student):
		global graduation_credits_object
		try:
			# we have credits requirements explicitly matching this student's class_year
			graduation_credits_object = super.depertmentgraduationcredits_set.get(class_year=student.class_of_year)
		except DepartmentGraduationCredits.DoesNotExist:
			# No explicit match, so find most recent requirement that went into effect *before* this marking period's
			# school year
			if  self.departmentgraduationcredits_set.filter(class_yrear__year__lt=student.class_of_year.year).order_by(
					'-class_year__year')[0]:
				graduation_credits_object = \
				self.departmentgraduationcredits_set.filter(class_year__year__lt=student.class_of_year.year).order_by(
					'-class_year__year')[0]
			elif IndexError:
				return None
		return graduation_credits_object

	class Meta:
		ordering = ('order_rank', 'name')

	def __str__(self):
		return self.name

class Address(models.Model):
	address_1 = models.CharField(max_length=250)
	address_2 = models.CharField(max_length=255, blank=True)
	address_3 = models.CharField(max_length=255, blank=True)


	def __str__(self):
		return self.address_1

class School(models.Model):
	active = models.BooleanField(default=False, help_text="DANGER..!!!!!..If Marked this will be the default School Information System Wide...")
	name = models.CharField(max_length=200)
	address = models.CharField(max_length=250)
	school_type = models.CharField(max_length=25, choices=SCHOOL_TYPE_CHOICE, blank=True, null=True)
	students_gender = models.CharField(max_length=25, choices=SCHOOL_STUDENTS_GENDER, blank=True, null=True)
	ownership = models.CharField(max_length=25, choices=SCHOOL_OWNERSHIP, blank=True, null=True)
	classification = models.CharField(max_length=30, choices=SCHOOL_CATEGORY, blank=True, null=True)
	mission = models.TextField(blank=True, null=True)
	vision = models.TextField(blank=True, null=True)
	telephone = models.CharField(max_length=50, blank=True)
	school_email = models.EmailField(blank=True, null=True)
	school_logo = models.ImageField(blank=True, null=True, upload_to='school_info')

	def __str__(self):
		return self.name

class Subject(models.Model):
	name = models.CharField(max_length=255, unique=True)
	subject_code = models.CharField(max_length=10, blank=True, null=True, unique=True)
	is_selectable = models.BooleanField(default=False, help_text="select if subject is optional")
	graded = models.BooleanField(default=True, help_text='Teachers can submit grades for this course')
	description = models.CharField(max_length=255, blank=True)
	department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True,
								   help_text="the department associated with this subject")

	def __str__(self):
		return self.name

class Day(models.Model):
	dayOfWeek = (
		("1", 'Monday'),
		("2", 'Tuesday'),
		("3", 'Wednesday'),
		("4", 'Thursday'),
		("5", 'Friday'),
		("6", 'Saturday'),
		("7", 'Sunday'),
	)
	day = models.CharField(max_length=1, choices=dayOfWeek, unique=True)
	def __str__(self):
		return self.day
	class Meta:
		ordering = ('day',)


# noinspection PyTypeChecker
class AcademicYear(models.Model):
	"""
	a db table row that maps on every academic year
	"""
	name = models.CharField(max_length=255, unique=True)
	start_date = models.DateField()
	end_date = models.DateField(blank=True)
	graduation_date = models.DateField(blank=True, null=True, help_text="The date when students graduate")
	#week_days = models.ManyToManyField(Day)
	active_year = models.BooleanField(help_text="DANGER!! This is the current school year. There can only be one and setting this will remove it from other years. " \
				  "If you want to change the active year you almost certainly want to click Admin, Change School Year.")

	class Meta:
		ordering = ('-start_date',)

	def __str__(self):
		return self.name

	@property
	def status(self, now_=date.today()):
		if self.active_year:
			return "active"
		elif self.start_date <= now_ >= self.end_date:
			return "ended"

		elif self.start_date > now_ < self.end_date:
			return "pending"

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		super(AcademicYear, self).save()
		if self.active_year:
			# if it is marked as the current year the update all the tables row i the database with false
			AcademicYear.objects.exclude(pk=self.pk).update(active_year="False")

##################################################################################################################################

class ImportLog(models.Model):
	"""
	 Keep a log of each time a user attempts to import a file, if successful store a database backup
	Backup is a full database dump and should not be thought of as a easy way to revert changes.
	"""

	user = models.ForeignKey(User, editable=False,on_delete=models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	import_file = models.FileField(upload_to='imported_files')
	database_backup = models.FileField(blank=True, null=True, upload_to="db_dumps")
	user_note = models.CharField(max_length=1024, blank=True)
	errors = models.BooleanField()

	def delete(self, using=None, keep_parents=False):
		""" These logs files would get huge if not deleted often"""
		if self.database_backup and os.path.exists(self.database_backup.path):
			os.remove(self.database_backup.path)
		if self.import_file and os.path.exists(self.import_file.path):
			os.remove(self.import_file.path)
		super(ImportLog, self).delete()


class Person(models.Model):
	"""Generic Person model. A person is any person in the School, such as parent,
	 student or teacher. Its's not login user though may be related to login user"""
	inactive = models.BooleanField(default=False)
	username = models.CharField(unique=True, max_length=250)
	first_name = models.CharField(max_length=300, verbose_name="First Name")
	last_name = models.CharField(max_length=300, verbose_name="Last Name")
	nationality = CountryField(blank=True)
	gender = models.CharField(max_length=10, choices=GENDER_CHOICE, blank=True)
	email = models.EmailField(blank=True, null=True)

	class Meta:
		ordering = ('first_name', 'last_name')

	@property
	def deleted(self):
		# for backward compatibility
		return self.inactive

class PhoneNumber(models.Model):
	PhoneTypeChoice = (
		('H', 'Home'),
		('C', 'Cell'),
		('W', 'Work'),
		('O', 'Other'),
	)
	number = models.CharField(max_length=150)
	ext = models.CharField(max_length=10, blank=True, null=True)
	type_ = models.CharField(max_length=1, choices=PhoneTypeChoice)
	note = models.CharField(max_length=255, blank=True)

	class Meta:
		abstract = True

	def full_number(self):
		if self.ext:
			return self.number + "x" + self.ext
		else:
			return self.number

class EmergencyContact(models.Model):
	f_name = models.CharField(max_length=255, verbose_name="First Name")
	m_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='Middle Name')
	l_name = models.CharField(max_length=255, verbose_name='Last Name')
	relationship_to_student = models.CharField(max_length=50, blank=True)
	street = models.CharField(max_length=255, blank=True, null=True, help_text="include apt number")
	city = models.CharField(max_length=255, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	primary_contact = models.BooleanField(default=True, help_text='This contact is where mailings and sms should be dent to')
	emergency_only = models.BooleanField(help_text="Only contact in case of emergency")

	class Meta:
		ordering = ('primary_contact', 'emergency_only', 'l_name')
		verbose_name = "Student Contact"

	def __str__(self):
		return "{} {}".format(self.f_name, self.l_name)

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		super(EmergencyContact, self).save()
		self.cache_student_addresses()

	def cache_student_addresses(self):
		"""cache these for the student for primary contact only
				There is another check on Student in case all contacts where deleted"""

		if self.primary_contact:
			for student in self.student_set.all():
				student.parent_gurdian = self.f_name + " " + self.l_name
				student.city = self.city
				student.street = self.street
				student.state = self.state
				student.zip = self.zip
				student.parent_email = self.email
				student.save()

				for contact in student.emergency_contacts.exclude(pk=self.pk):
					# There should be one primary contact!
					if contact.primary_contact:
						contact.primary_contact = False
						contact.save()

			# cache those for the application
			if hasattr(self, 'application_set'):
				for applicant in self.application_set.all():
					applicant.set_cache(self)

class GradeLevel(models.Model):
	id = models.IntegerField(unique=True, primary_key=True, verbose_name='Grade Level')
	name = models.CharField(max_length=150, unique=True)

	class Meta:
		ordering = ('id',)

	def __str__(self):
		return self.name

class ClassYear(models.Model):
	""" Class year such as class of 2019"""
	year = models.CharField(max_length=100, unique=True, help_text="Example 2020")
	full_name = models.CharField(max_length=255, help_text="Example Class of 2020", blank=True)

	def __str__(self):
		return self.full_name

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		if not self.full_name:
			self.full_name = "Class of %s" % (self.year, )
		super(ClassYear, self).save()

class ReasonLeft(models.Model):
	reason = models.CharField(max_length=255, unique=True)

	def __str__(self):
		return self.reason

###############################################################################################################################

class Stream(models.Model):
	name = models.CharField(max_length=50, validators=[stream_validator])

	def __str__(self):
		return self.name

class Teacher(Person):
	teacher_id = models.CharField(max_length=255, unique=True)
	middle_name = models.CharField(max_length=100, blank=True)
	subject_specialization = models.ManyToManyField(Subject, blank=True)
	national_id = models.CharField(max_length=100, blank=True, null=True)
	address = models.CharField(max_length=255, blank=True)
	phone_number = models.CharField(max_length=150)
	alt_email = models.EmailField(blank=True, null=True, help_text="Personal Email apart from the one given by the school")
	date_of_birth = models.DateField(blank=True, null=True)
	designation = models.CharField(max_length=255, blank=True, null=True)
	image = models.ImageField(upload_to='Teacher_images', blank=True, null=True)


	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):

		#  check if the person is already a student
		if Student.objects.filter(id=self.id).count():
			raise ValidationError("cannot have a someone be a student and a Teacher")

		# save model
		super(Teacher, self).save()

		# create a user with default password as firstname and lastname
		user, created = User.objects.get_or_create(username=self.username)
		if created:
			user.password = (str(self.first_name) + str(self.last_name))
			user.save()
			# send the username and password to email
			msg = "\nHey {} Welcome to {}, your username is {} and the default one time password is {}" \
				  "Please login to your portal and change the password.." \
				  "This password is valid for 24 hours only".format((str(self.first_name) + str(self.last_name)), "this school ",self.username, user.password
																	)
			#mail_agent(self.alt_email, "Default user Name and password", msg)

		# add the user to a Group
		group, gcreated = Group.objects.get_or_create(name='teacher')
		if gcreated:
			group.save()
		user.groups.add(group)
		user.save()

class ClassRoom(models.Model):
	name = models.CharField(max_length=50)
	stream = models.ForeignKey(Stream, on_delete=models.CASCADE, blank=True, related_name='class_stream')
	class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)
	grade_level = models.ForeignKey(GradeLevel,blank=True, null=True, on_delete=models.SET_NULL, help_text="the grade level of the class ie: 'form one is in Grade one' ")
	capacity = models.IntegerField(help_text='Enter total number of sits default is set to 25', default=25, blank=True)
	occupied_sits = models.IntegerField(blank=True, null=True, default=0)

	class Meta:
		unique_together = ['name', 'stream']

	def __str__(self):
		if self.stream:
			return "{} {}".format(self.name, str(self.stream))
		else:
			return self.name

	def available_sits(self):
		open_sits = self.capacity - self.occupied_sits
		return open_sits

	def class_status(self):
		# get the percentage of occupied sits
		percentage = (self.occupied_sits / self.capacity) * 100
		return '{}%'.format(float(percentage))

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		"""
		Before we Save any data in the class room lets check to see if there are open sits

		:param force_insert:
		:param force_update:
		:param using:
		:param update_fields:
		:return:
		"""
		if (self.capacity - self.occupied_sits) < 0:
			raise ValueError("all sits in this classroom are occupied try other classes")
		else:
			super(ClassRoom, self).save()

class SubjectAllocation(models.Model):
	"""
	A model to allocate subjects to respective teacher t the school
	"""
	teacher_name = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='allocated_subjects')
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)
	class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='subjects')

	def __str__(self):
		return str(self.teacher_name)

	def subjects_data(self):
		for data in self.subjects.all():
			return data

class Parent(Person):
	"""

	"""
	middle_name = models.CharField(max_length=50, null=True, blank=True)
	parent_type = models.CharField(choices=Parent_CHOICE, max_length=10)
	address = models.CharField(max_length=255,blank=True)
	phone_number = models.CharField(max_length=150, help_text='personal phone number')
	national_id = models.CharField(max_length=100, blank=True, null=True)
	occupation = models.CharField(max_length=255, blank=True, help_text="current occupation")
	monthly_income = models.FloatField(help_text="parents average monthly income", blank=True)
	single_parent = models.BooleanField(default=False, blank=True, help_text="is he/she a single parent")
	alt_email  = models.EmailField(blank=True, null=True, help_text="personal Email ")
	date = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to='Parent_images', blank=True)

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		super(Parent, self).save()

		# create a user and password
		user, created = User.objects.get_or_create(username=self.username)
		if created:
			user.password = (str(self.first_name) + str(self.last_name))
			user.save()

		# lets create a student group or add to an existing one
		group, gcreated = Group.objects.get_or_create(name="parent")
		if gcreated:
			group.save()
		user.groups.add(group)
		user.save()

class Student(Person):
	unique_id = models.AutoField(primary_key=True)
	middle_name = models.CharField(max_length=50, blank=True)
	graduation_date = models.DateField(blank=True, null=True)
	grade_level = models.ForeignKey(GradeLevel, blank=True, null=True, on_delete=models.SET_NULL)
	class_of_year = models.ForeignKey(ClassYear, blank=True, null=True, on_delete=models.SET_NULL)
	date_dismissed = models.DateField(blank=True, null=True)
	reason_left = models.ForeignKey(ReasonLeft,blank=True, null=True, on_delete=models.SET_NULL)
	religion = models.CharField(max_length=50, blank=True, null=True)
	blood_group = models.CharField(max_length=10, blank=True, null=True)
	parent_guardian = models.ForeignKey(Parent, on_delete=models.CASCADE, blank=True, related_name='child')
	date_of_birth = models.DateField()
	admission_date = models.DateTimeField(auto_now_add=True)
	admission_number = models.CharField(max_length=50, blank=True, unique=True)
	image = models.ImageField(upload_to='StudentsImages', blank=True)

	cache_gpa = models.DecimalField(editable=False, max_digits=5, decimal_places=2, blank=True, null=True)

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)


	def get_year(self, active_year):
		""" get the year (fresh, etc) from the class of XX year"""

		if self.class_of_year:
			try:
				this_year = active_year.end_date.year
				school_last_year = GradeLevel.objects.oder_by('-id')[0].id
				class_of_year = self.class_of_year.unique_for_year

				target_year = school_last_year - (class_of_year - this_year)
				return GradeLevel.objects.get(id=target_year)
			except:
				return None

	def determine_year(self):
		""" Set the year (fresh, etc) from class XX year"""

		if self.class_of_year:
			try:
				active_year = AcademicYear.objects.filter(active_year=True)[0]
				self.year = self.get_year(active_year)
			except:
				return None


	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

		# 1. Check if there is a staff with the same id as student
		if Teacher.objects.filter(id=self.id).count():
			raise ValidationError('Cannot have someone be a student and a Staff')

		self.admission_number = assign_admission_numbers()
		self.determine_year()

		super(Student, self).save()
		user, created = User.objects.get_or_create(username=self.username)
		if created:
			# if a user is created give the user a default password
			user.password = (str(self.first_name) + str(self.middle_name))
			user.save()

		# lets create a student group or add to an existing one
		group, gcreated = Group.objects.get_or_create(name="students")
		if gcreated:
			group.save()
		user.groups.add(group)
		user.save()

	def clean(self):
		"""Check if a Faculty exists, cant have someone be a student and faculty"""
		if Teacher.objects.filter(id=self.id).count():
			raise ValidationError('Cannot have someone be a student AND faculty!')
		super(Student, self).clean()

	def graduate_and_create_alumni(self):
		self.inactive = True

		self.reason_left = ReasonLeft.objects.get_or_create(reason="Graduated")[0]
		if not self.graduation_date:
			self.graduation_date = date.today()

		# register student as Alumni
		# noinspection PyUnresolvedReferences
		#from alumni.models import Alumni
		#Alumni.objects.get_or_create(student=self)
		self.save()

class StudentClass(models.Model):
	"""
	This is a bridge table to link a student to a class
	when you add a student to a class we update the selected class capacity

	"""
	classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='class_student')
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_class')

	@property
	def is_current_class(self):
		if self.academic_year.is_current_session:
			return True
		return False

	def __str__(self):
		return str(self.student_id)

	def update_class_table(self):
		selected_class = ClassRoom.objects.get(pk=self.classroom.pk)
		new_value = selected_class.occupied_sits + 1
		selected_class.occupied_sits = new_value
		selected_class.save()

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		# lets update the class sits

		self.update_class_table()
		super(StudentClass, self).save()

class StudentsMedicalHistory(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	history = models.TextField()
	file = models.FileField(upload_to='students_medical_files', blank=True, null=True)

	def __str__(self):
		return str(self.student)


class StudentsPreviousAcademicHistory(models.Model):
	students_name = models.ForeignKey(Student, on_delete=models.CASCADE)
	former_school = models.CharField(max_length=255, help_text="Former school name")
	last_gpa = models.FloatField()
	notes = models.CharField(max_length=255, blank=True, help_text="Indicate students academic performance according to your observation")
	academic_record = models.FileField(upload_to='students_former_academic_files', blank=True)

	def __str__(self):
		return str(self.students_name)

class CarryOverStudent(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
	stream = models.ForeignKey(Stream, on_delete=models.CASCADE, blank=True, null=True)
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)

	def __str__(self):
		return str(self.student)

class RepeatingStudent(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)

	def __str__(self):
		return str(self.student)

class Result(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	gpa = models.FloatField(null=True)
	cat_gpa = models.FloatField(null=True)
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)

	def __str__(self):
		return str(self.student)



class Dormitory(models.Model):
	name = models.CharField(max_length=150)
	capacity = models.PositiveIntegerField(blank=True, null=True)
	occupied_beds = models.IntegerField(blank=True, null=True)
	captain = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True)

	def __str__(self):
		return self.name

	def available_beds(self):
		total = self.capacity - self.occupied_beds
		if total <= 0:
			return "all beds in {} are occupied".format(self.name)

		else:
			return total

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):

		if (self.capacity - self.occupied_beds) <= 0:
			raise  ValueError("all beds in {} are occupied:\n please add more beds or save to another dormitory".format(self.name))
		else:
			super(Dormitory, self).save()

class DormitoryAllocation(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE)
	date_from = models.DateField(auto_now_add=True)
	date_till = models.DateField(blank=True, null=True)

	def __str__(self):
		return str(self.student.admission_number)


	def update_dormitory(self):
		"""
		update the capacity of each dorm
		:return:
		"""
		selected_dorm = Dormitory.objects.get(pk=self.dormitory.pk)
		new_capacity = selected_dorm.occupied_beds + 1
		selected_dorm.occupied_beds = new_capacity
		selected_dorm.save()


	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		self.update_dormitory()
		super(DormitoryAllocation, self).save()

class ExaminationListHandler(models.Model):
	name = models.CharField(max_length=100)
	start_date = models.DateField()
	ends_date = models.DateField()
	out_of = models.IntegerField()
	#academic_term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name='academic_term_exam')
	classrooms = models.ManyToManyField(ClassRoom, related_name='class_exams')
	comments = models.CharField(max_length=200, blank=True, null=True, help_text="Comments Regarding Exam")
	created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	created_on = models.DateTimeField(auto_now_add=True)

	@property
	def status(self):
		if datetime.now().date() > self.start_date:
			return "Done"
		elif self.start_date >= datetime.now().date() >= self.ends_date:
			return "on going"
		return "Coming up"

	def __str__(self):
		return self.name

	def save(self, force_insert=False, force_update=False, using=None,
			 update_fields=None):
		super(ExaminationListHandler, self).save()

class MarksManagement(models.Model):
	exam_name = models.ForeignKey(ExaminationListHandler, on_delete=models.CASCADE, related_name='exam_marks')
	points_scored = models.FloatField()
	subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subject_marks')
	student = models.ForeignKey(StudentClass, on_delete=models.CASCADE, related_name='student_marks')
	created_by = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='marks_entered')
	date_time = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.points_scored

class TranscriptNoteChoice(models.Model):
	"""
	Returns a predefined transcript note.
	when displayed from 'TranscriptNote':
	replaces $student with student name
	Replaces $he_she with students appropriate gender word
	"""

	note = models.TextField()

	def __str__(self):
		return self.note

class TranscriptNote(models.Model):
	""" These are notes intended to be shown on a transcript. They may be either free
		text or a predefined choice. If both are entered they will be concatenated.
		"""

	note = models.TextField(blank=True)
	predefined_note = models.ForeignKey(TranscriptNoteChoice, blank=True, null=True, on_delete=models.SET_NULL)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.student)

class StudentFile(models.Model):
	file = models.FileField(upload_to='student_files')
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.student)

class StudentHealthRecord(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	record = models.TextField()

	def __str__(self):
		return str(self.student)

class MessageToParent(models.Model):
	"""Store a message to be shown to parents for a specific amount of time"""

	message = models.TextField(help_text="this message will be shown to Parents when they log in")
	start_date = models.DateField(default=timezone.now, help_text="If blank the message will be posted starting today")
	end_date = models.DateField(default=timezone.now, help_text="if blank the message will end today")

	def __str__(self):
		return self.message

class FamilyAccessUser(User):
	""" A person who can log into the non-admin side and see the same view as a student,
		except that he/she cannot submit timecards.
		This proxy model allows non-superuser registrars to update family user accounts.
		"""

	class Meta:
		proxy = True

	def save(self, *args, **kwargs):
		super(FamilyAccessUser, self).save()
		self.groups.add(Group.objects.get_or_create(name='family')[0])
