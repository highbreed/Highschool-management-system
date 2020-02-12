from django.contrib import messages
from django.forms import modelformset_factory, formset_factory, inlineformset_factory
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
import datetime

from .forms import ClassroomDateQueryForm, StudentsAttendanceForm, StudentAttendanceForm
# noinspection PyUnresolvedReferences
from DB.models import StudentClass, ClassRoom, Student
from .models import StudentAttendance

# add logging capabilities to the attendance function and SMS features

def student_attendance_manager(request):
	"""
	this function is responsible for querying the attendance parameters and present the student multiple attendance form
	"""
	if request.method == "POST":
		# get the class name , the attendance date  and present the attendance form

		class_name = get_object_or_404(ClassRoom, pk=request.POST['class_name']) # class name
		attendance_date = request.POST['date_field'] # date

		# get the students in the class which is current active
		students = StudentClass.objects.filter(main_class=class_name)

		# modelform creation
		# noinspection PyPep8Naming
		AttendanceFormset= modelformset_factory(StudentAttendance, form=StudentsAttendanceForm, extra=students.count())

		msg = ""

		# initiate the form and pass in the required parameters ie: classroom_id, attendance_date

		initial = []
		enroll_notes = []
		for student in students:
			student.marked = False
			initial.append(
				{'student': student.id, 'status': None, 'notes': None, 'attendance_date': attendance_date})
			enroll_notes.append("")

		formset = AttendanceFormset(initial=initial, queryset=StudentAttendance.objects.none())

		# add notes to each form
		i = 0
		form_students = students
		for form in formset.forms:
			form.enroll_note = enroll_notes[i]
			form.student_display = form_students[i]
			i += 1

		# add form to each student, so we can use for student in students in the template
		i = 0
		forms = formset.forms
		for student in students:
			if not student.marked:
				student.form = forms[i]
				i += 1


		template = 'attendance/students_attendance_form.html'

		context = {
			'class_name':class_name,
			'msg': msg,
			'formset': formset,
			'students': students,
		}

		return JsonResponse({'html_form': render_to_string(template, context, request=request)})
	else:
		# send in the selection form

		template = 'attendance/students_attendance_manager.html'
		class_date_selector_form = ClassroomDateQueryForm(request.GET or None)
		context = {
			'choice_form': class_date_selector_form
		}
		return render(request, template, context)

def student_attendance_register(request):
	if request.method == "POST":
		students = StudentClass.objects.filter(main_class=request.GET['class_id'])
		StudentsAttendanceFormSet = modelformset_factory(StudentAttendance, form=StudentsAttendanceForm, extra=students.count())
		list_formset = StudentsAttendanceFormSet(request.POST)
		if list_formset.is_valid():
			list_formset.save()

			# sms feature for all absent students
			return JsonResponse({"message":"Success"})
		else:
			msg = "\nDuplicate entry detected! It's possible someone else is entering " \
				  "attendance for these students at the same time. Please confirm attendance." \
				  " If problems persist contact an administrator."
			return JsonResponse({"success": False, "message": msg})
	else:
		# if the request is not post return an error message
		msg = "\nThe request method is Not Post"
		return JsonResponse({'success': False, 'message': msg})

def teacher_attendance(request, course=None):
	""" Take attendance. show course selection if there is more than one course
	"""
	today = datetime.date.today()
	students = StudentClass.objects.filter(main_class=1)

	readonly = False
	msg = ""
	AttendanceFormset = modelformset_factory(
		StudentAttendance, form=StudentAttendanceForm,
		extra=students.count())

	if request.method == 'POST':
		formset = AttendanceFormset(request.POST)
		if formset.is_valid():
			for form in formset.forms:
				object = form.save()

				# don't log first

			messages.success(request, 'Attendance recorded')
			return HttpResponse('saved')
		else:
			msg = "\nDuplicate entry detected! It's possible someone else is entering " \
				  "attendance for these students at the same time. Please confirm attendance." \
				  " If problems persist contact an administrator."
			return HttpResponse(formset.errors)

	initial = []
	enroll_notes = []
	for student in students:
		student.marked = False
		initial.append({'student': student.id, 'status': None, 'notes': None, 'attendance_date': datetime.date.today()})
		#note = student.courseenrollment_set.filter(course=course)[0].attendance_note
		enroll_notes.append("")

	formset = AttendanceFormset(initial=initial, queryset=StudentAttendance.objects.none())

	# add notes to each form
	i = 0
	form_students = students
	for form in formset.forms:
		form.enroll_note = enroll_notes[i]
		form.student_display = form_students[i]
		i += 1

	# add form to each student, so we can use for student in students in the template
	i = 0
	forms = formset.forms
	for student in students:
		if not student.marked:
			student.form = forms[i]
			i += 1

	return render(
		request,
		'attendance/test.html',
		{
			'request': request,
			#'readonly': readonly,
			'msg': msg,
			'formset': formset,
			'students': students, }

	)

def student_attendance_report(request):

	# query the db and return attendance for the selected class
	if request.method == 'POST':
		class_name = get_object_or_404(ClassRoom, pk=request.POST['class_name'])  # class name
		attendance_date = request.POST['date_field']  # date

		# get the students in the class which is current active

		# check if the student is current active

		students_attendance = StudentAttendance.objects.filter(attendance_date=attendance_date)
		students = Student.objects.filter(student_attendance__in=students_attendance)

		# check if we have the student_attendance report
		if students.count():
			pass
		else:
			msg = "\nNo attendance Report for The Class and date selected" \
				  "Please check on the date and class and submit again"
			return JsonResponse({'success':False, 'message': msg})

		template = 'attendance/attendance_report_template.html'
		context = {
			'class_name': class_name,
			'students_attendance': students_attendance,
		}
		return JsonResponse({'html_form': render_to_string(template, context, request=request)})


	else:
		# send in the selection form

		template = 'attendance/students_attendance_report.html'
		class_date_selector_form = ClassroomDateQueryForm(request.GET or None)
		context = {
			'choice_form': class_date_selector_form
		}
		return render(request, template, context)
