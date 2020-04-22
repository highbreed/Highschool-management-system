from  django.shortcuts import render
from django.http import JsonResponse

from ..models import Period, MarkingPeriod, SubjectPeriod
# noinspection PyUnresolvedReferences
from DB.models import Subject, ClassRoom


def timetable_manager_view(request):
    get_periods = Period.objects.all()
    template = 'timetabler/manager_view.html'
    context = {
        'school_periods':  get_periods,
    }
    return render(request, template, context)

def create_timetable_view(request):
    school_periods = Period.objects.all()
    print(school_periods)


def update_timetable_view(request, table_id):
    pass


def delete_timetable_view(request, table_id):
    pass


def detail_timetable_view(request, table_id):
    pass
