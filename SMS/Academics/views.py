from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse


from .forms import ClassRoomRegForm, StreamRegForm, SubjectRegForm\
	, SubjectAllocationForm, ExaminationRegForm
# noinspection PyUnresolvedReferences
from DB.models import ClassRoom, Stream, Student, StudentClass\
	, Subject,  SubjectAllocation, AcademicYear, Term, StudentAttendance\
	,ExaminationListHandler, Teacher


def class_management(request):
	class_room_qs = ClassRoom.objects.all()
	context = {
		'class_rooms':class_room_qs,
	}
	template = 'class_management_temp/class_management.html'
	return render(request, template, context)

def add_class(request):
	class_form = ClassRoomRegForm()
	if request.method == 'POST':
		class_form = ClassRoomRegForm(request.POST)
		if class_form.is_valid():
			class_form.save()
			messages.info(request, 'New class added')
			return redirect('/academic/')
		else:
			messages.info(request, class_form.errors['name'])
		return redirect('/academic/add_new_class/')
	else:
		template = 'class_management_temp/add_class.html'
		context = {
			'class_form': class_form,
		}
		return 	JsonResponse({'html_form':render_to_string(template, context, request=request)})

def edit_class_room(request, slug):
	if request.method == 'POST':
		classroom_inst = get_object_or_404(ClassRoom, pk=slug)
		class_form = ClassRoomRegForm(request.POST, instance=classroom_inst)
		if class_form.is_valid():
			class_form.save()
			messages.info(request, '{} updated successful'.format(classroom_inst))
			return redirect('/academic/')
		else:
			return HttpResponse(class_form.errors)
	else:
		classroom_inst = get_object_or_404(ClassRoom, pk=request.GET['post_id'])
		class_form = ClassRoomRegForm(instance=classroom_inst)
		template = 'class_management_temp/edit_classroom.html'
		context = {
			'class_form': class_form,
			'class_room':classroom_inst
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def classroom_view(request, slug):
	# db query
	classroom_qs = get_object_or_404(ClassRoom, pk=slug) # lets get the classroom object
	students_qs = StudentClass.objects.filter(main_class=classroom_qs)  # query the student who's class allocated == to our classroom object

	# student list
	class_students_list = []

	# get the students who's academic year is current active and append to our list
	for student_data in students_qs:
		if student_data.academic_year.is_current_session:
			class_students_list.append(student_data)

	context = {
		'classroom':classroom_qs,
		'class_students': class_students_list,
	}
	template = 'class_management_temp/classroom_details.html'
	return render(request, template, context)

def stream_management(request):
	stream_qs = Stream.objects.all()
	template = 'class_management_temp/stream_management.html'
	context = {
		'streams': stream_qs,
	}
	return render(request, template, context)

def add_stream(request):
	if request.method == 'POST':
		stream_form = StreamRegForm(request.POST)
		if stream_form.is_valid():
			stream_form.save()
			messages.info(request, 'stream {} saved'.format(stream_form.cleaned_data['name']))
			return redirect('/academic/streams/')
		else:
			messages.info(request, stream_form.errors['name'])
			return redirect('/academic/streams/')
	else:
		stream_form = StreamRegForm()
		template = 'class_management_temp/add_stream.html'
		context = {
			'class_form': stream_form,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def edit_stream(request, slug):
	if request.method == "POST":
		stream_inst = get_object_or_404(Stream, pk=slug)
		stream_form = StreamRegForm(request.POST, instance=stream_inst)
		if stream_form.is_valid():
			stream_form.save()
			messages.info(request, "{} edited successful".format(stream_inst))
			return redirect("/academic/streams/")
		else:
			messages.info(request, stream_form.errors['name'])
			return redirect("/academic/streams/")
	else:
		stream_inst = get_object_or_404(Stream, pk=request.GET['post_id'])
		stream_form = StreamRegForm(instance=stream_inst)
		context = {
			'class_form':stream_form,
			'stream': stream_inst,
		}
		template = 'class_management_temp/edit_stream.html'
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def subject_management(request):
	subject_qs = Subject.objects.all()
	context = {
		'subjects':subject_qs,
	}
	template = 'class_management_temp/subject_management.html'
	return render(request, template, context)

def add_subject(request):
	if request.method == 'POST':
		subject_form = SubjectRegForm(request.POST)
		if subject_form.is_valid():
			subject_form.save()
			messages.info(request, "{} added successful".format(subject_form.cleaned_data['name']))
			return redirect('/academic/subjects/')
		else:
			messages.info(request, subject_form.errors['name'])
			return redirect('/academic/subjects/')
	else:
		subject_form = SubjectRegForm()
		template = 'class_management_temp/add_subject.html'
		context = {
			'subject_form':subject_form,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def edit_subject(request, slug):
	if request.method == "POST":
		subject_inst = get_object_or_404(Subject, pk=slug)
		subject_form = SubjectRegForm(request.POST, instance=subject_inst)
		if subject_form.is_valid():
			subject_form.save()
			messages.info(request, "{} edited successfully".format(subject_inst))
			return redirect('/academic/subjects/')
		else:
			messages.info(request, subject_form.errors['name'])
			return redirect('/academic/subjects/')
	else:
		subject_inst = get_object_or_404(Subject, pk=request.GET['post_id'])
		subject_form = SubjectRegForm(instance=subject_inst)
		template = 'class_management_temp/edit_subject.html'
		context = {
			'subject_form':subject_form,
			'subject':subject_inst,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def class_subjects(request):
	classroom_qs = ClassRoom.objects.all()
	template = 'class_management_temp/class_subject.html'
	context = {
		'classrooms':classroom_qs,
	}
	return render(request, template, context)

def get_subjects(request):
	allocated_subjects = []
	subject_qs = SubjectAllocation.objects.filter(class_room=request.GET['post_id'])
	for objects in subject_qs:
		if objects.academic_year.is_current_session:
			allocated_subjects.append(objects)
	template = 'subject_management_temp/subject_table.html'
	context = {
		'data':allocated_subjects,
	}
	return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def add_class_subject(request, slug):
	"""
	Lets allocate subjects to classes
	:param request:
	:param slug:
	:return:
	"""

	if request.method == "POST":
		class_inst = get_object_or_404(ClassRoom, pk=slug) # get the class instance
		subject_allocation_form = SubjectAllocationForm(request.POST)
		if subject_allocation_form.is_valid():
			subject_form = subject_allocation_form.save(commit=False)
			# link the classroom instance
			subject_form.class_room = class_inst
			subject_form.save() # save the form
			messages.info(request, "{} added successful to {}".format(subject_allocation_form.cleaned_data['subject'], class_inst))
			return redirect('/academic/class_subjects/')
		else:
			messages.info(request, subject_allocation_form.errors['name'])
			return redirect('/academic/class_subjects/')
	else:
		class_inst = get_object_or_404(ClassRoom, pk=request.GET['post_id'])
		subject_allocation_form = SubjectAllocationForm()
		template = 'subject_management_temp/subject_allocation_form.html'
		context = {
			'form':subject_allocation_form,
			'classroom':class_inst,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def edit_class_subject(request, slug):
	if request.method == "POST":
		subject_inst = get_object_or_404(SubjectAllocation, pk=slug)
		subject_form = SubjectAllocationForm(request.POST, instance=subject_inst)
		if subject_form.is_valid():
			subject_form.save()
			messages.info(request, "{} edited successfully".format(subject_inst))
			return redirect('/academic/subjects/')
		else:
			messages.info(request, subject_form.errors['name'])
			return redirect('/academic/subjects/')
	else:
		subject_inst = get_object_or_404(SubjectAllocation, pk=request.GET['post_id'])
		subject_form = SubjectAllocationForm(instance=subject_inst)
		template = 'class_management_temp/edit_subject.html'
		context = {
			'subject_form':subject_form,
			'subject':subject_inst,

		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def examination_management(request):
	exams_list_qs = ExaminationListHandler.objects.all()
	template = 'exam_management_temp/exam_management.html'
	context = {
		'exam_list':exams_list_qs,
	}
	return render(request, template, context)

def add_examination(request):
	if request.method == 'POST':
		exam_form = ExaminationRegForm(request.POST)
		if exam_form.is_valid():
			exam_form.save()
			messages.info(request, "{} added Successful".format(exam_form.cleaned_data['name']))
			return redirect('/academic/exam_management/')
		else:
			messages.info(request, "Input Error: {} could not be added,"
								   " please check your details and add again".format(exam_form.cleaned_data['name']))
			return redirect('/academic/exam_management/')
	else:
		exam_form = ExaminationRegForm()
		template = 'exam_management_temp/add_exam.html'
		context = {
			'exam_form': exam_form,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})

def edit_examination(request, slug):
	if request.method == "POST":
		exam_inst = get_object_or_404(ExaminationListHandler, pk=slug)
		exam_form = ExaminationRegForm(request.POST, instance=exam_inst)
		if exam_form.is_valid():
			exam_form.save()
			messages.info(request, "{} edited successfully".format(exam_form.cleaned_data['name']))
			return redirect('/academic/exam_management/')
		else:
			messages.info(request, "{} not edited check your information and enter "
								   "again".format(exam_form.cleaned_data['name']))
			return redirect('/academic/exam_management/')
	else:
		exam_inst = get_object_or_404(ExaminationListHandler, pk=request.GET['post_id'])
		exam_form = ExaminationRegForm(instance=exam_inst)
		template = 'exam_management_temp/edit_exam.html'
		context = {
			'exam_form':exam_form,
			'exam': exam_inst,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request)})
