from django import forms
# noinspection PyUnresolvedReferences
from DB.models import  ClassRoom
from .models import StudentAttendance, AttendanceStatus


class StudentsAttendanceForm(forms.ModelForm):
	class Meta:
		model = StudentAttendance
		fields = '__all__'
		#exclude = [
			#'siqned_by',
		#]


class StudentAttendanceForm(forms.ModelForm):
	class Meta:
		model = StudentAttendance
		fields = ('student', 'attendance_date', 'notes', 'status')
		widgets = {
			'student': forms.HiddenInput(
				attrs={'tabindex': "-1", 'class': 'student_select', 'onfocus': "this.defaultIndex=this.selectedIndex;",
					   'onchange': "this.selectedIndex=this.defaultIndex;"}),
			'attendance_date': forms.HiddenInput(),
			'notes': forms.TextInput(attrs={'tabindex': "-1", }),
		}

	status = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'status', }),
									queryset=AttendanceStatus.objects.filter(teacher_selectable=True))


class ClassroomDateQueryForm(forms.Form):

	class_name = forms.ModelChoiceField(queryset=ClassRoom.objects.all(), help_text='Select a class')
	date_field = forms.DateField()

	widgets = {
		'date_field': forms.DateInput(attrs={'id': 'datetimepicker'})
	}

