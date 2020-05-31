from django import forms
from django.forms.widgets import CheckboxSelectMultiple, Select
# noinspection PyUnresolvedReferences
from DB.models import Student, Parent, Address, Teacher, \
	StudentClass, SubjectAllocation, ClassRoom


GENDER_CHOICE = (
	('M', 'Male'),
	('F', 'Female'),

)


class DateInput(forms.DateInput):
	input_type = 'date'


class StudentForm(forms.ModelForm):
	medical_history = forms.CharField(max_length=1000, required=True, help_text="Students medical history")
	medical_file = forms.FileField(required=False, help_text="Doctors signed medical report")
	class_room = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), help_text="Classroom Allocation")
	former_school = forms.CharField(max_length=255, required=True, help_text="Former school name")
	former_gpa = forms.FloatField(help_text="previous recent gpa")
	notes = forms.CharField(help_text="academic observation and recommendation", max_length=500)
	academic_records = forms.FileField(help_text="former academic records", required=True)

	class Meta:
		model = Student
		fields = ['first_name','middle_name', 'last_name', 'gender', 'nationality',
				  'grade_level', 'religion', 'blood_group', 'date_of_birth', 'image',
				  ]
		widgets = {
			'date_of_birth': forms.DateInput(attrs={'id': 'datetimepicker'})
		}


class ParentForm(forms.ModelForm):
	address = forms.CharField(max_length=255, required=True, help_text='resident address')
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
		fields = ['classroom',]


class TeacherForm(forms.ModelForm):
	class Meta:
		model = Teacher
		fields = [
			'first_name', 'middle_name', 'last_name', 'gender', 'date_of_birth', 'nationality',
			'national_id', 'image', 'subject_specialization', 'designation',
			 'address', 'alt_email', 'phone_number'
		]
		widgets = {
			'subject_specialization': CheckboxSelectMultiple(),
			'date_of_birth': forms.DateInput(attrs={'id': 'datetimepicker'})
		}



class TeacherSubjectForm(forms.ModelForm):
	class Meta:
		model = SubjectAllocation
		fields = '__all__'
		widgets = {
			'subjects': CheckboxSelectMultiple(),
		}

