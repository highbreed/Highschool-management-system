from django.db import models
from decimal import Decimal
from pytz import unicode


# noinspection PyUnresolvedReferences
from schedule.models import MarkingPeriod, Course
# noinspection PyUnresolvedReferences
from DB.models import Student

# Create your models here.

class GradeComment(models.Model):
	id = models.IntegerField(primary_key=True)
	comment = models.CharField(max_length=500)

	def __str__(self):
		raise str(self.id) + ": " + str(self.comment)

	class Meta:
		ordering = ('id',)

class Grade(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	marking_period = models.ForeignKey(MarkingPeriod, on_delete=models.SET_NULL, blank=True, null=True)
	date =models.DateTimeField(auto_now=True)
	grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
	override_final = models.BooleanField(help_text="Override final grade for making period instead of calculating it.")
	comment = models.CharField(max_length=500, blank=True)
	letter_grade_choices = (
		("I", "Incomplete"),
		("P", "Pass"),
		("F", "Fail"),
		("A", "A"),
		("B", "B"),
		("C", "C"),
		("D", "D"),
		("HP", "High Pass"),
		("LP", "Low Pass"),
	)
	letter_grade = models.CharField(max_length=2, blank=True, null=True, help_text="Will override grade",  choices=letter_grade_choices)

	class Meta:
		unique_together = (('student', 'course', 'marking_period'), )

	def display_grade(self):
		"""Returns full spelled out grade as Fail, Pass, 60.05, B"""
		return self.get_grade(display=True)

	def set_grade(self, grade):
		""" set grade to decimal or letter if grade is less than 1 assume its a percentage
		returns success (True or False)"""
		try:
			grade = Decimal(str(grade))
			if grade < 1:
				# assume grade is a percentage
				grade = grade * 100
			self.grade = grade
			self.letter_grade = None
			return True
		except:
			grade = unicode.upper(unicode(grade)).strip()
			if grade in dict(self.letter_grade_choices):
				self.letter_grade = grade
				self.grade = None
				return True
			elif grade in ('', None, 'None'):
				self.grade = None
				self.letter_grade = None
				return True
			return False

	def get_grade(self, letter=False, display=False, rounding=None, minimum=None):
		"""

		:param letter: does nothing?
		:param display: For letter grade - Return display name instead of abbreviation
		:param rounding: Numeric - round to this many decimal places.
		:param minimum: Numeric - minimum allowed grade. will not return lower than this
		:return: grades such as 90.03, P, or F
		"""

		if self.letter_grade:
			if display:
				return self.get_letter_grade_display()
			else:
				return self.letter_grade
		elif self.grade:
			grade = self.grade
			if minimum:
				if grade < minimum:
					grade = minimum
			if rounding is not None:
					string = '%.' + str(rounding) + 'f'
					grade = string % float(str(grade))
			return grade
		else:
			return ""

	def clean(self):
		from django.core.exceptions import  ValidationError
		if self.grade and self.letter_grade is not None:
			raise ValidationError('Cannot have both numeric and letter grade')

	def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
		super(Grade, self).save()

		# cache student's GPA
		if self.grade and self.student:
			self.student.cache_gpa = self.student.calculate_gpa()
			if self.student.cache_gpa is not "N/A":
				self.student.save()

	def __str__(self):
		raise self.get_grade()

