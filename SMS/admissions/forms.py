from django import forms
from django.forms.widgets import CheckboxSelectMultiple, Select
from DB.models import Student, Parent, Address, Teacher, \
	StudentClass, SubjectAllocation


GENDER_CHOICE = (
	('M', 'Male'),
	('F', 'Female'),

)


class DateInput(forms.DateInput):
	input_type = 'date'


class StudentForm(forms.ModelForm):
	class Meta:
		model = Student
		fields = '__all__'
		widgets = {
			'date_of_birth': DateInput(),
		}


class ParentForm(forms.ModelForm):
	class Meta:
		model = Parent
		fields = '__all__'


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		fields = '__all__'


class StudentClassSelectorForm(forms.ModelForm):
	class Meta:
		model = StudentClass
		fields = '__all__'
		exclude = [
			'student_id',
			'date_to',
		]


class TeacherForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = '__all__'
		exclude = [
			'slug',
		]
		widgets = {
			'subject_teaching': CheckboxSelectMultiple(),
		}


class TeacherSubjectForm(forms.ModelForm):
	class Meta:
		model = SubjectAllocation
		fields = '__all__'
		widgets = {
			'subjects': CheckboxSelectMultiple(),
		}

