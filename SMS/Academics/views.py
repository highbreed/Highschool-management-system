from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .forms import ClassRoomRegForm, StreamRegForm, ClassStreamForm, SchoolRegForm, SubjectRegForm
from DB.models import ClassRoom, Stream, ClassStream


# Create your views here.


def class_management(request):
	"""
	this function is responsible for adding new
	classrooms and streams to the database
	:param request:
	:return:
	"""
	if request.method == 'POST':
		class_form = ClassRoomRegForm(request.POST)
		if class_form.is_valid():
			class_form.save()
			return redirect('/academic/')
		else:
			messages.info(request, 'Class already exists')
		return redirect('/academic/')
	else:
		class_form = ClassRoomRegForm()
		stream_form = StreamRegForm()
		class_link = ClassStreamForm()
		class_stream = ClassStream.objects.all()
		class_room = ClassRoom.objects.all()
		context = {
			'class_form': class_form,
			'stream_form': stream_form,
			'link_form': class_link,
			'stream_view': class_stream,
			'class_rooms': class_room,
		}

		template = 'class_management.html'

		return render(request, template, context)


def add_stream(request):
	if request.method == 'POST':
		stream_form = StreamRegForm(request.POST)
		if stream_form.is_valid():
			stream_form.save()

			messages.info(request, 'stream saved')
			return redirect('/academic/add_streams/')
		else:
			messages.info(request, stream_form.errors['name'])
			return redirect('/academic/add_streams/')

	else:
		stream_form = StreamRegForm()
		template = 'add_stream.html'
		context = {
			'form': stream_form,
		}
		return render(request, template, context)


def link_class_stream(request):
	if request.method == 'POST':
		link_form = ClassStreamForm(request.POST)
		if link_form.is_valid():
			link_form.save()
			messages.info(request, 'New classroom added')
			return redirect('/academic/link_class_stream/')
		else:
			messages.info(request, link_form.errors)
			return redirect('/academic/link_class_stream/')
	else:
		link_form = ClassStreamForm()
		template = 'link_class.html'
		context = {
			'link_form': link_form,
		}
		return render(request, template, context)


def class_view(request):
	class_stream = ClassStream.objects.all()
	template = 'class_view.html'
	context = {
		'stream_view': class_stream,
	}

	return render(request, template, context)


def add_class(request):
	class_form = ClassRoomRegForm()
	if request.method == 'POST':
		class_form = ClassRoomRegForm(request.POST)
		if class_form.is_valid():
			class_form.save()
			messages.info(request, 'New class added')
			return redirect('/academic/add_new_class/')
		else:
			messages.info(request, class_form.errors['name'])
		return redirect('/academic/add_new_class/')
	return render(request, 'add_class.html', {'class_form': class_form})


def add_subjects(request):
	if request.method == 'POST':
		subject_form = SubjectRegForm(request.POST)
		if subject_form.is_valid():
			subject_form.save()
			messages.info(request, '{} subject has been added'.format(subject_form.cleaned_data['name']))
			return redirect('/academic/add_subjects/')
		else:
			messages.info(request, subject_form.errors['name'])
		return redirect('/academic/add_subjects/')
	else:
		subject_form = SubjectRegForm()
		template = 'add_subject.html'
		context = {
			'subject_form': subject_form,
		}

		return render(request, template, context)
