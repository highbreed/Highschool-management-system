from django.shortcuts import render
from django.forms import modelformset_factory
from django.http import JsonResponse, HttpResponse
# noinspection PyUnresolvedReferences
from DB.models import AcademicYear
from django.template.loader import render_to_string

from .models import SchoolEvent, MarkingPeriod, Period
from .forms import AcademicYearSetup, AddSchoolEventForm\
	, MarkingPeriodForm, SchoolInfoForm

from .selector import get_current_school_information

# Create your views here.

def schedule_dashboard(request):
	academic_year = AcademicYear.objects.all()
	template = 'schedule/dashboard.html'
	context = {
		'academic_year': academic_year,
	}
	return render(request, template, context)

def add_academic_year(request):
	if request.method == 'POST':
		academic_year_form = AcademicYearSetup(request.POST or None)
		if academic_year_form.is_valid():
			academic_year_form.save()
			msg = '\n New Academic year saved'
			return JsonResponse({'success': True, 'message': msg})
		else:
			print(academic_year_form.errors)
			msg = '\nFailed: \n New Academic year cannot be saved' \
				  'This may be a result of duplicates or year with the same name exists' \
				  'Check your data and try again'
			return JsonResponse({'success': False, 'message': msg})
	else:
		academic_year_form = AcademicYearSetup()
		template = 'schedule/academic_year_form.html'
		context = {
			'academic_year_form': academic_year_form
		}
		return JsonResponse({'html_form': render_to_string(template, context, request)})

def school_calender(request):
	active_academic_year = AcademicYear.objects.get(active_year=True)
	template = 'schedule/calender.html'
	context = {
		'academic_year': active_academic_year,
	}
	return render(request, template, context)

def add_events(request):
	if request.method == 'POST':
		form = AddSchoolEventForm(request.POST or None)

		academic_year = AcademicYear.objects.get(active_year=True)
		if form.is_valid():
			school_event = SchoolEvent()
			school_event.title = form.cleaned_data['title']
			school_event.start = form.cleaned_data['start']
			school_event.end = form.cleaned_data['end']
			school_event.notes = form.cleaned_data['notes']
			school_event.academic_year = academic_year
			school_event.save()

			msg = "\nEvent added Successful"
			return JsonResponse({'success': True, 'message': msg})
		else:

			msg = "\nForm is not Valid!!!, this may be due to duplication or incorrect date format Please Check your data " \
				  "and submit again"
			return JsonResponse({'success':False, 'message': msg})

	else:
		date_selected = request.GET['post_id']
		form = AddSchoolEventForm()
		context = {
			'form': form,
			'start_date': date_selected
		}
		template = 'schedule/event_schedule.html'
		return JsonResponse({'html_form': render_to_string(template, context, request=request)})

# noinspection PyUnresolvedReferences
def get_events(request):
	import json
	from django.core.serializers.json import DjangoJSONEncoder
	"""Implement this function latter
	NB: this will handle querring events for the system calender"""

	from_date = request.GET['start'] # events from date
	to_date = request.GET['end'] # events to date
	cur = AcademicYear.objects.get(active_year=True) # current active year
	events_qs = SchoolEvent.objects.filter(academic_year=cur,
										   start__gte=from_date, end__lte=to_date).values('title', 'start', 'end') # query the events
	data = json.dumps(list(events_qs), cls=DjangoJSONEncoder)

	return HttpResponse(data)

def add_marking_period(request):
	if request.method == "POST":
		print('post request')
		form = MarkingPeriodForm(request.POST or None)
		print(form)
		if form.is_valid():
			print('Valid')
			form.save()
			msg = '\nNew Semester Added Successfully'
			return JsonResponse({'success': True, 'message': msg})
		else:
			print('Not Valid')
			msg = '\nError..!!!Cant add semester..this maybe due to duck typing or duplication ' \
				  '\nPlease Check your Information and Try Again..'
			return JsonResponse({'success':False, 'message': msg})
	else:
		form = MarkingPeriodForm()
		context = {
			'form': form,
		}
		template = 'schedule/marking_period_form.html'
		return JsonResponse({'html_form': render_to_string(template, context, request=request)})

# noinspection PyUnresolvedReferences
def marking_period_dsh(request):

	academic_year_qs = AcademicYear.objects.get(active_year=True)
	marking_period_qs = MarkingPeriod.objects.filter(academic_year=academic_year_qs).order_by('sort_order')

	total_marking_periods = marking_period_qs.count()

	template = 'schedule/marking_period_dsh.html'
	context = {
		'academic_year': academic_year_qs,
		'total_years': 1,
		'marking_period': marking_period_qs,
		'total_marking_period': total_marking_periods,
	}
	return render(request, template, context)

def add_periods(request):
	"""
	this function is responsible for adding daily school periods for the system
	:param request:
	:return:
	"""
	PeriodFormSet = modelformset_factory(Period, fields='__all__' )

	if request.method == 'POST':
		formset = PeriodFormSet(request.POST)
		### you have to implement validation
		formset.save()
		return JsonResponse({'success':True, 'message':"Period added Successfully"})
	else:
		formset = PeriodFormSet()
		context = {
			'period_form': formset,
		}
		template = 'schedule/period_setup.html'
		return render(request, template, context)

def get_school_information(request):
	qs = get_current_school_information()
	context = {
		'school_qs':qs
	}
	template = 'schedule/school_info_manager.html'
	return render(request, template, context)

def add_school_information(request):
	if request.method == 'POST':
		form = SchoolInfoForm(request.POST or None)
		if form.is_valid():
			form.save()
			msg = "\nInformation Updated Successfully"
			return JsonResponse({'success':True, 'message': msg})
		else:
			msg = "\nError Please correct on {} and try again".format(form.errors['name'])
			return JsonResponse({'success':False, 'message':msg})
	else:
		school_info_form = SchoolInfoForm()
		template = 'schedule/school_info_form.html'
		context = {
			'form': school_info_form,
		}
		return JsonResponse({'html_form': render_to_string(template, context, request=request)})




