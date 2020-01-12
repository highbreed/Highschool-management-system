from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from DB.models import School, Subject, ClassRoom, Stream, ClassStream


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


class ClassLinkForm(forms.Form):

	class_name = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), help_text='Choose a class')
	stream_name = forms.ModelChoiceField(queryset=Stream.objects.all(), help_text='select a stream')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))


class ClassStreamForm(forms.ModelForm):
	class Meta:
		model = ClassStream
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.form_method = 'post'
		self.helper.add_input(Submit('submit', 'Save'))
