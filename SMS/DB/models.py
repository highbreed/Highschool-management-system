from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils.text import slugify
from .validators import class_room_validator, subject_validator, stream_validator, students_date_of_birth_validator, \
	ASCIIUsernameValidator
from admissions.scripts import assign_admission_numbers

A = "A"
B = "B"
C = "C"
D = "D"
F = "F"
PASS = "PASS"
FAIL = "FAIL"

GRADE = (
	(A, 'A'),
	(B, 'B'),
	(C, 'C'),
	(D, 'D'),
	(F, 'F'),
)

COMMENT = (
	(PASS, "PASS"),
	(FAIL, "FAIL"),
)

ACADEMIC_TERM = (
	("ONE", "One"),
	("TWO", "Two"),
	("THREE", "Three"),
)

GENDER_CHOICE = (
	('M', 'Male'),
	('F', 'Female'),
	('Other', 'Other')
)

SCHOOL_TYPE_CHOICE = (
	('boarding school', 'boarding school'),
	('day school', 'day school'),
	('boarding-day school', 'boarding-day school')
)

SCHOOL_STUDENTS_GENDER = (
	('Boys School', 'Boys School'),
	('Girl School', 'Girl School'),
	('Mixed', 'Mixed'),
)

SCHOOL_OWNERSHIP = (
	('Government', 'Government'),
	('Private', 'Private'),
)

SCHOOL_CATEGORY = (
	('National', 'National'),
	('Extra County', 'Extra County'),
	('County', 'County'),
	('Sub County', 'Sub County'),
)


class Address(models.Model):
	address = models.CharField(max_length=250)
	email = models.EmailField(null=True, blank=True)
	phone_number = models.CharField(max_length=15)

	def __str__(self):
		return self.address


class School(models.Model):
	name = models.CharField(max_length=200)
	address = models.ForeignKey(Address, on_delete=models.PROTECT, blank=True, null=True)
	school_type = models.CharField(max_length=25, choices=SCHOOL_TYPE_CHOICE, blank=True, null=True)
	students_gender = models.CharField(max_length=25, choices=SCHOOL_STUDENTS_GENDER, blank=True, null=True)
	ownership = models.CharField(max_length=25, choices=SCHOOL_OWNERSHIP, blank=True, null=True)
	classification = models.CharField(max_length=30, choices=SCHOOL_CATEGORY, blank=True, null=True)
	mission = models.TextField(blank=True, null=True)
	vision = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.name


class Subject(models.Model):
	name = models.CharField(max_length=50, validators=[subject_validator])
	subject_code = models.CharField(max_length=10, blank=True, null=True)
	is_selectable = models.BooleanField(default=False, blank=True, null=True)

	def __str__(self):
		return self.name


class User(AbstractUser):
	is_student = models.BooleanField(default=False)
	is_lecturer = models.BooleanField(default=False)
	is_parent = models.BooleanField(default=False)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
	picture = models.ImageField(upload_to="user_pictures/", blank=True, null=True)

	username_validator = ASCIIUsernameValidator()

	def get_picture(self):
		"""
		function to retun the users profile pic or an avatar
		:return:
		"""
		no_picture = settings.STATIC_URL + 'img/img_avatar.png'
		try:
			return self.picture.url
		except:
			return no_picture

	def get_full_name(self):
		full_name = self.username
		if self.first_name and self.last_name:
			full_name = self.first_name + " " + self.last_name
		return full_name


class AcademicYear(models.Model):
	"""
	a db table row that maps on every academic year
	"""
	session = models.CharField(max_length=200, unique=True)
	is_current_session = models.BooleanField(default=False, blank=True, null=True)
	next_session_begins = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.session


class Term(models.Model):
	"""
	a db row that maps on a term to the academic year
	"""
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True)
	is_current_term = models.BooleanField(default=False, blank=True, null=True)
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True, null=True)
	term_ends_on = models.DateField(blank=True, null=True)
	next_term_begins = models.DateField(null=True, blank=True)

	def __str__(self):
		return self.term



class Stream(models.Model):
	name = models.CharField(max_length=50, validators=[stream_validator])

	def __str__(self):
		return self.name


class Teacher(models.Model):
	teacher_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, blank=True)
	last_name = models.CharField(max_length=100)
	subject_teaching = models.ManyToManyField(Subject, blank=True)
	nationality = models.CharField(max_length=100 ,blank=True, null=True)
	national_id = models.CharField(max_length=100, blank=True, null=True)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True)
	slug = models.SlugField(blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICE)

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.slug = slugify(self.first_name + self.last_name)
		super(Teacher, self).save()

	def __str__(self):
		return "{} {}".format(self.first_name[0], self.last_name)


class ClassRoom(models.Model):
	name = models.CharField(max_length=50)
	stream_id = models.ForeignKey(Stream, on_delete=models.CASCADE, blank=True, related_name='class_stream')
	subjects = models.ManyToManyField(Subject, blank=True)
	class_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True)
	capacity = models.IntegerField(help_text='Enter total number of sits defaults is set to 25', default=25, blank=True)
	occupied_sits = models.IntegerField(blank=True, null=True, default=0)

	def __str__(self):
		if self.stream_id:
			return "{} {}".format(self.name, str(self.stream_id))
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
	subjects = models.ManyToManyField(Subject, related_name='allocated_subjects')
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)
	class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.teacher_name)

	def subjects_data(self):
		for data in self.subjects.all():
			return data


class Parent(models.Model):
	Parent_CHOICE = (
		('F', 'Father'),
		('M', 'Mother'),
		('G', 'Guardian'),

	)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50)
	parent_type = models.CharField(choices=Parent_CHOICE, max_length=1)
	address = models.ForeignKey(Address, on_delete=models.CASCADE, blank=True, null=True)
	nationality = models.CharField(max_length=100, blank=True, null=True)
	national_id = models.CharField(max_length=100, blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)


class Student(models.Model):
	GENDER_CHOICE = (
		('M', 'Male'),
		('F', 'Female'),

	)
	unique_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=50)
	middle_name = models.CharField(max_length=50, blank=True)
	last_name = models.CharField(max_length=50)
	gender = models.CharField(choices=GENDER_CHOICE, max_length=1, null=False)
	parent = models.ForeignKey(Parent, on_delete=models.CASCADE, blank=True)
	date_of_birth = models.DateField(validators=[students_date_of_birth_validator])
	admission_date = models.DateTimeField(auto_now_add=True)
	admission_number = models.CharField(max_length=50, blank=True)
	image = models.ImageField(upload_to='StudentsImages', blank=True)

	def __str__(self):
		return "{} {}".format(self.first_name, self.last_name)

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.admission_number = assign_admission_numbers()
		super(Student, self).save()


class StudentClass(models.Model):
	"""
	This is a bridge table to link a student to a class
	when you add a student to a class we update the selected class capacity

	"""

	student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_class')
	main_class = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
	date_from = models.DateField(auto_now_add=True)
	date_to = models.DateField(blank=True, null=True)

	def __str__(self):
		return str(self.student_id)

	def student_class(self):
		# this method returns the class a student is in
		return str(self.main_class)

	def update_class_table(self):
		selected_class = ClassRoom.objects.get(pk=self.main_class.pk)
		new_value = selected_class.occupied_sits + 1
		selected_class.occupied_sits = new_value
		selected_class.save()

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		# lets update the class sits

		self.update_class_table()
		super(StudentClass, self).save()


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


class SchoolEvent(models.Model):
	name = models.CharField(max_length=150)
	academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, blank=True)
	term = models.CharField(max_length=10, choices=ACADEMIC_TERM, blank=True, null=True)
	starts_on = models.DateField()
	ends_on = models.DateField(blank=True, null=True)

	def __str__(self):
		return self.name


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
