from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from datetime import date


def students_date_of_birth_validator(value):
	"""
	this function is responsible o validating the students date of birth
	if the students year of  birth is less than or equal to least_year_of_birth
	then we raise a validation error
	:imports Student from models
	:param value:
	:return:
	"""
	from .models import Student
	required_age = 12
	least_year_of_birth = date.today().year - required_age

	if value.year >= least_year_of_birth:
		raise ValidationError(_('not valid date, student should be at least 13 years of age..!!!'))
