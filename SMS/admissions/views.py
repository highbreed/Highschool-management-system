from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string
from .forms import ParentForm, StudentForm, \
	AddressForm, TeacherForm, StudentClassSelectorForm
# noinspection PyUnresolvedReferences
from DB.models import  ClassRoom, Student, SubjectAllocation, StudentClass, Stream, Teacher, Parent


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
		class_selector_form = StudentClassSelectorForm(request.POST, prefix='class_selector_form')
		# lets check to see if all forms are valid
		if all([student_form.is_valid(), parent_form.is_valid(),
				class_selector_form.is_valid()]):

			student = student_form.save(commit=False)
			parent = parent_form.save(commit=False)
			student_class = class_selector_form.save(commit=False)

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

		if teacher_form.is_valid():
			teacher = teacher_form.save()
			messages.info(request, "{} added successfully".format(teacher))
			return redirect('/admissions/teachers/')

		else:
			print('NOT Valid')
			return HttpResponse('Not valid')

	else:
		teacher_form = TeacherForm(prefix='teacher_form')

		template = 'teachers_admissions/teacher_admission.html'
		ajax_template = 'teachers_admissions/js-teacher_admission.html'
		context = {
			'teacher_form': teacher_form,
		}
		if request.is_ajax():
			html_form = render_to_string(ajax_template, context, request=request)
			return JsonResponse({'html_form':html_form})
		else:
			return render(request, template, context)


def teacher_information_update(request, slug):
	"""
	A function that is responsible for updating of teachers info
	:param request:
	:param slug:
	:return:
	"""
	if request.method == "POST":
		teacher_qs = get_object_or_404(Teacher, pk=slug)
		teacher_form = TeacherForm(request.POST, instance=teacher_qs)
		if teacher_form.is_valid():
			teacher = teacher_form.save()
			messages.info(request, '{} information edited successfully'.format(teacher))
			return redirect('/admissions/teachers/')
		else:
			#messages.info(request, 'Invalid data')
			return HttpResponse(teacher_form.errors)
	else:
		teacher_qs = get_object_or_404(Teacher, pk=request.GET['post_id'])
		teacher_form = TeacherForm(instance=teacher_qs)
		context = {
			'teacher_form':teacher_form,
			'teacher':teacher_qs
		}
		ajax_template = 'teachers_admissions/teacher_info_update.html'
		if request.is_ajax():
			html_form = render_to_string(ajax_template, context, request=request)
			return JsonResponse({'html_form': html_form})
		else:
			return render(request, ajax_template, context)


def teacher_details(request):
	teacher_qs = get_object_or_404(Teacher, pk=request.GET['post_id'])
	context = {
		'teacher':teacher_qs
	}
	template = "teachers_admissions/teachers_details.html"
	if request.is_ajax():
		html_form = render_to_string(template, context,request=request)
		return JsonResponse({'html_form':html_form})
	else:
		return render(request,template, context)


def teacher_delete(request):
	return JsonResponse({'html_form':request})


def teachers_view(request):
	"""
	this view function is responsible for
	showing teachers information
	:param request:
	:return:
	"""
	teachers_qs = Teacher.objects.all()
	template = "teachers_view.html"
	context = {
		"teachers":teachers_qs,
	}
	# check if our request is an ajax request
	# if so we return a json response
	if request.is_ajax():
		json = serializers.serialize('json', context) # serialize the data with django serializers
		return JsonResponse(json)
	else:
		return render(request, template, context)


def parent_list(request):
	"""

	:param request:
	:return:
	"""
	parents_qs = Parent.objects.all()
	template = 'parents_temp/parents_view.html'
	context = {
		'parents':parents_qs,
	}
	return render(request, template, context)


def parents_details(request):
	parent_qs = get_object_or_404(Parent, pk=request.GET['post_id'])
	template = 'parents_temp/parents_details.html'
	context = {
		'parent':parent_qs,
	}
	html_form = render_to_string(template, context, request=request)
	return JsonResponse({'html_form': html_form})


def parent_update(request, slug):
	if request.method == "POST":
		parent_inst = get_object_or_404(Parent, pk=slug)
		parent_form = ParentForm(request.POST, instance=parent_inst)
		if parent_form.is_valid():
			parent_form.save()
			messages.info(request, "{} edited successfully".format(parent_inst))
			return redirect('/admissions/parents/')
		else:
			return HttpResponse(parent_form.errors)
	else:
		parent_inst = get_object_or_404(Parent, pk=slug)
		parent_form = ParentForm(instance=parent_inst)
		context = {
			'parent_form':parent_form,
			'parent':parent_inst,
		}
		template = 'parents_temp/parents_update.html'
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})


def student_view(request):
	"""
	a function to view student list
	:param request:
	:return:
	"""

	student_qs = Student.objects.all()
	context = {
		'students': student_qs,
	}
	template = 'students_temp/students_view.html'
	return render(request, template, context)


def student_details(request):
	"""
	this is a function to view student details,
	takes in the admission number as slug and
	query the db for any student with the same admission number
	:param request:
	:return:
	"""
	student_qs = get_object_or_404(Student, pk=request.GET['post_id']) # get the student instance or return 404 Error
	template = 'students_temp/student_details.html'
	context = {
		'student': student_qs,
	}
	return JsonResponse({'html_form': render_to_string(template, context, request=request)})


def student_update(request, slug):
	if request.method == "POST":
		student_inst = get_object_or_404(Student, pk=slug)
		student_form = StudentForm(request.POST, instance=student_inst, prefix='student_form' )
		parent_form = ParentForm(request.POST, prefix='parent_form', instance=student_inst.parent)
		if all([student_form.is_valid(), parent_form.is_valid()]):
			parent = parent_form.save()
			student = student_form.save(commit=False)
			# link parent to student
			student.parent = parent
			student.save()

			messages.info(request, "{}\'s information updated successfully".format(student_inst))
			return redirect('/admissions/students_view/')
		else:
			return HttpResponse(parent_form.errors)

	else:
		student_inst = get_object_or_404(Student, pk=request.GET['post_id'])
		student_form = StudentForm(prefix='student_form', instance=student_inst)
		parent_form = ParentForm(prefix='parent_form', instance=student_inst.parent)
		context = {
			'student_form': student_form,
			'parent_form': parent_form,
			'student': student_inst,
		}
		template = 'students_temp/student_info_update.html'
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})
