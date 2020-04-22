import datetime


def assign_admission_numbers():
	from DB.models import Student
	school_initial = 'STGHS'
	this_year = datetime.datetime.now().year
	admission = []
	default_value = str(school_initial) + '/' + '001' + '/' + str(this_year)
	if Student.objects.all().count() == 0:
		return default_value
	else:
		student_number = Student.objects.all().last().pk + 1

	if student_number < 10:
		new_admission = '{}{}{}'.format(0, 0, student_number)
		admission.append(new_admission)
	elif student_number < 100:
		new_admission = '{}{}'.format(0, student_number)
		admission.append(new_admission)
	else:
		admission.append(student_number)
	return '{}/{}/{}'.format(school_initial, admission[0], this_year)



