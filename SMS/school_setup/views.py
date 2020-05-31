from django.shortcuts import render
from django.http import JsonResponse

from .forms import SchoolInfoForm

# Create your views here.

def add_school_information(request):
	if request.method == "POST":
		school_form = SchoolInfoForm(request.POST)
		if school_form.is_valid():
			school_form.save()
			msg = "\nSchool Information updated successfully"
			return JsonResponse({'success':True, 'message':msg })
		else:
			msg = '\nInformation Not Valid please Check your Information and try again'
			return JsonResponse({'success':False, 'message':msg })
	else:
		school_form = SchoolInfoForm()
		template = 'school_setup/school_info.html'
		context = {
			'form':school_form,
		}
		return render(request, template, context)