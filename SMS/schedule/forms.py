from django import forms
# noinspection PyUnresolvedReferences
from DB.models import AcademicYear, Day, School

from .models import SchoolEvent, MarkingPeriod


class AcademicYearSetup(forms.ModelForm):

	class Meta:
		model = AcademicYear
		fields = '__all__'

		widgets = {
			'start_date': forms.DateInput(attrs={'id': 'start-date-picker', 'placeholder': '2020-01-30'}),
			'end_date': forms.DateInput(attrs={'id': 'end-date-picker', 'placeholder': '2020-01-30'}),
			'graduation_date': forms.DateInput(attrs={'id': 'graduation-date-picker', 'placeholder': '2020-01-30'}),
		}


class AddSchoolEventForm(forms.ModelForm):
	class Meta:
		model = SchoolEvent
		exclude = ['academic_year']

		widgets = {
			'end': forms.DateInput(attrs={'id': 'end-date-picker', 'placeholder': '2020-01-30'}),
			'start': forms.DateInput(attrs={'id': 'start-date-picker', 'placeholder': '2020-01-30'}),
		}

class MarkingPeriodForm(forms.ModelForm):
	class Meta:
		model = MarkingPeriod
		fields = '__all__'

		widgets = {
			'start_date': forms.DateInput(attrs={'id': 'start-date-picker'}),
			'end_date': forms.DateInput(attrs={'id': 'end-date-picker'}),
			'grade_posting_begins': forms.DateInput(attrs={'id': 'grade_posting_begins-picker'}),
			'grade_posting_ends': forms.DateInput(attrs={'id': 'grade_posting_ends-picker'})

		}


class SchoolInfoForm(forms.ModelForm):
	class Meta:
		model = School
		fields = '__all__'