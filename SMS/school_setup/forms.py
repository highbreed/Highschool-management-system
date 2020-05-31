from django import forms

# noinspection PyUnresolvedReferences
from DB.models import School


class SchoolInfoForm(forms.ModelForm):
	class Meta:
		model = School
		fields = '__all__'

