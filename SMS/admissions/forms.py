from django import forms
from django.forms.widgets import CheckboxSelectMultiple, Select
from DB.models import Student, Parent, Address, Teacher, \
	StudentClass, SubjectAllocation, ClassTeachers


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


class TeacherSubjectForm(forms.ModelForm):
	class Meta:
		model = SubjectAllocation
		fields = '__all__'
		widgets = {
			'subjects': CheckboxSelectMultiple(),
		}


class ClassTeacherForm(forms.ModelForm):
	class Meta:
		model = ClassTeachers
		fields = '__all__'
		widgets = {
			'stream_id': Select()
		}