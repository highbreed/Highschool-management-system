# noinspection PyUnresolvedReferences
from DB.models import School


def get_current_school_information():

    school_info_qs = School.objects.filter(active=True)

    return school_info_qs