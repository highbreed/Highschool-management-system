from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
import datetime
from .forms import ParentForm, StudentForm, \
	AddressForm, TeacherForm, StudentClassSelectorForm, TeacherSubjectForm
from DB.models import  ClassRoom, Student, SubjectAllocation, StudentClass, Stream


def dashboard(request):
	"""
	this is the index of admission app...
	shows school admissions info
	:param request:
	:return:
	"""
	total_school_capacity = []
	class_rooms = ClassRoom.objects.all()

	# lets get the school_capacity and all available vacancies
	for data in class_rooms:
		total_school_capacity.append(data.capacity)

	# lets get the total_number of students in the school
	students_total = len(Student.objects.all())

	template = 'admission_dashboard.html'
	context = {
		'class_rooms': class_rooms,
		'school_capacity': sum(total_school_capacity),
		'students_total': students_total,
		'vacancies': sum(total_school_capacity) - students_total,
	}
	return render(request, template, context)


def class_room_view(request, slug):
	"""
	this function takes in the pk of classroom as an argument and
	returns all data associated with the classroom
	:param request:
	:param slug:
	:return:
	"""
	class_room = get_object_or_404(ClassRoom, pk=slug)

	# get class statistics
	student_class = StudentClass.objects.filter(main_class=class_room)

	context = {
		'class_name': class_room,
		'students': (data.student_id for data in student_class),
	}
	template = 'class_room_details.html'
	return render(request, template, context)


def student_admission(request):
	"""
	a function to handle student admission process
	it takes in parent and address data then links it to the database
	:param request:
	:return:
	"""
	if request.method == 'POST':
		student_form = StudentForm(request.POST, request.FILES,prefix='student_form')
		parent_form = ParentForm(request.POST,  prefix='parent_form')
		address_form = AddressForm(request.POST, prefix='address_form')
		class_selector_form = StudentClassSelectorForm(request.POST, prefix='class_selector_form')
		# lets check to see if all forms are valid
		if all([student_form.is_valid(), parent_form.is_valid(), address_form.is_valid(),
				class_selector_form.is_valid()]):

			student = student_form.save(commit=False)
			parent = parent_form.save(commit=False)
			address = address_form.save()
			student_class = class_selector_form.save(commit=False)

			# lets link the parent and address
			parent.address = address
			parent.save()

			# lets link the student and parent
			student.parent = parent
			student.save()

			# lets assign a class to the student

			student_class.student_id = student
			student_class.save()

			messages.info(request, "{} has been admitted successfully".format(student))
			if 'save' in request.POST:
				return redirect('/admissions/')
			elif 'save and add another' in request.POST:
				return redirect('/admissions/students_admission/')
			else:
				return HttpResponse('Edit form')
		else:
			return HttpResponse('form not valid')

	else:
		student_form = StudentForm(prefix='student_form')
		parent_form = ParentForm(prefix='parent_form')
		address_form = AddressForm(prefix='address_form')
		class_selector_form = StudentClassSelectorForm(prefix='class_selector_form')

		template = 'student_admission.html'

		context = {
			'student_form': student_form,
			'parent_form': parent_form,
			'address_form': address_form,
			'class_selector_form': class_selector_form,
		}

		return render(request, template, context)


def teacher_admission(request):
	"""
	this function helps in the admission of new teachers
	:param request:
	:return:
	"""

	if request.method == 'POST':
		teacher_form = TeacherForm(request.POST,request.FILES, prefix='teacher_form')
		address_form = AddressForm(request.POST, prefix='address_form')
		teacher_subject_form = TeacherSubjectForm(request.POST, prefix='teacher_subject')
		if all([teacher_form.is_valid(), address_form.is_valid(), teacher_subject_form.is_valid()]):
			teacher = teacher_form.save(commit=False)
			address = address_form.save()

			# lets link the teacher with the address
			teacher.address = address
			teacher.save()

			# lets link the teachers subjects
			teacher_subject = teacher_subject_form.save(commit=False)
			teacher_subject.teacher_name = teacher
			teacher_subject.save()

			return HttpResponse('Thank you')
		else:
			print('NOT Valid')
			return HttpResponse('Not valid')

	else:
		teacher_form = TeacherForm(prefix='teacher_form')
		address_form = AddressForm(prefix='address_form')
		teacher_subject_form = TeacherSubjectForm(prefix='teacher_subject')

		template = 'teachers_admissions/teacher_admission.html'
		context = {
			'teacher_form': teacher_form,
			'address_form': address_form,
			'teacher_subject': teacher_subject_form,
		}

		return render(request, template, context)


def student_details(request):
	"""
	function to show the students details
	:param request:
	:return:
	"""
	if request.method == "GET":
		student_id = request.GET['student_pk']
		print('requested')
		return HttpResponse('sucess')
	else:
		return HttpResponse('fuck you')
