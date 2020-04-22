from django.shortcuts import render
from DB.models import  ClassRoom, Student, Teacher


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
	students_total = Student.objects.all().count()

	template = 'dashboard.html'
	context = {
		'class_rooms': class_rooms,
		'school_capacity': sum(total_school_capacity),
		'students_total': students_total,
		'vacancies': sum(total_school_capacity) - students_total,
	}
	return render(request, template, context)