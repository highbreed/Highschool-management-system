from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
import datetime
from .forms import ParentForm, StudentForm, \
	AddressForm, TeacherForm, StudentClassSelectorForm, TeacherSubjectForm, ClassTeacherForm
from DB.models import ClassStream, ClassRoom, Student, SubjectAllocation



def dashboard(request):
	total_school_capacity = []
	class_rooms = ClassRoom.objects.all()
	class_stream = ClassStream.objects.all()

	# lets get the school_capacity and all available vacancies
	for data in class_rooms:
		total_school_capacity.append(data.capacity)

	# lets get the total_number of students in the school
	students_total = len(Student.objects.all())

	template = 'admission_dashboard.html'
	context = {
		'class_rooms': class_rooms,
		'class_streams': class_stream,
		'school_capacity': sum(total_school_capacity),
		'students_total': students_total,
		'vacancies': sum(total_school_capacity) - students_total,
	}
	return render(request, template, context)


def class_stream_view(request, slug):
	stream = get_object_or_404(ClassStream, pk=slug)

	# get class statistics
	class_subjects = []
	class_data_sets = [['Empty Sits', stream.available_sits], ['Occupied Sits', stream.occupied_sits]]
	student_class = SubjectAllocation.objects.filter(class_stream=stream)
	class_subjects_qs = SubjectAllocation.objects.filter(class_id=stream)
	for data in class_subjects_qs:
		for subject in data.subject_id.all():
			class_subjects.append(subject)

	context = {
		'class_sits': class_data_sets,
		'class_name': stream,
		'students': (data.student_id for data in student_class),
		'subject_dataset': class_subjects,
	}
	template = 'class_stream_details.html'
	return render(request, template, context)


def student_admission(request):
	"""
	a function to handle student admission process
	it takes in parent and address data then links it to the database
	:param request:
	:return:
	"""
	if request.method == 'POST':
		student_form = StudentForm(request.POST, prefix='student_form')
		parent_form = ParentForm(request.POST, prefix='parent_form')
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
		teacher_form = TeacherForm(request.POST, prefix='teacher_form')
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


def class_teacher(request):
	"""
	a function that assigns each stream with a class teacher
	:param request:
	:return:
	"""
	if request.method == 'POST':
		class_teacher_form = ClassTeacherForm(request.POST, prefix='class_teacher_form')
		if class_teacher_form.is_valid():
			class_teacher_form.save()
			return HttpResponse('Thank You')
		else:
			return HttpResponse('form not valid')
	else:
		class_teacher_form = ClassTeacherForm(prefix='class_teacher_form')
		template = 'teachers_admissions/class_teacher.html'
		context = {
			'class_form': class_teacher_form,
		}
		return render(request, template, context)
