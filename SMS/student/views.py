from django.shortcuts import render
from DB.models import Student
from django.shortcuts import get_object_or_404

# Create your views here.


def student_details(request ,slug):
	"""
	this is a function to view student details,
	takes in the admission number as slug and
	query the db for any student with the same admission number
	:param request:
	:param slug:
	:return:
	"""
	student_qs = get_object_or_404(Student, pk=slug)

	template = 'student_details.html'
	context = {
		'student': student_qs,
	}

	return render(request, template, context)