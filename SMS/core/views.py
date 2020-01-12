from django.shortcuts import render


def index(request):
	"""
	our dashboard index page
	:param request:
	:return:
	"""
	template = 'index.html'
	return render(request, template)