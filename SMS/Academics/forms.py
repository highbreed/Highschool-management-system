from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
# noinspection PyUnresolvedReferences
from DB.models import School, Subject, ClassRoom, Stream\
	,  SubjectAllocation, ExaminationListHandler
from django.forms import CheckboxSelectMultiple


class SchoolRegForm(forms.ModelForm):
	class Meta:
		model = School
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))


class SubjectRegForm(forms.ModelForm):
	class Meta:
		model = Subject
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))


class ClassRoomRegForm(forms.ModelForm):
	class Meta:
		model = ClassRoom
		fields = '__all__'
		widgets = {
			'subjects': CheckboxSelectMultiple(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))


class StreamRegForm(forms.ModelForm):
	class Meta:
		model = Stream
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))


class ClassRoomSelector(forms.Form):

	class_name = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), help_text='Choose a class')
	attendance_date = forms.DateField(help_text="select the date to register")


class SubjectAllocationForm(forms.ModelForm):
	class Meta:
		model = SubjectAllocation
		fields = '__all__'
		exclude = [
			'class_room',
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))

class ExaminationRegForm(forms.ModelForm):
	class Meta:
		model = ExaminationListHandler
		fields = '__all__'
		exclude = [
			'created_by',
		]
		widgets = {
			'classrooms': CheckboxSelectMultiple(),
			'start_on_date': forms.DateInput(attrs={'id': 'datetimepicker12', 'placeholder':'2020-01-30'}),
			'ends_on_date': forms.DateInput(attrs={'id': 'datetimepicker', 'placeholder':'2020-01-30'}),
		}