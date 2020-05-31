from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import NoticeBoard
from .forms import NotificationForm
# Create your views here.

def notification_manager(request):
	# query all the notifications in db and display

	notification_qs = NoticeBoard.objects.all()
	template = 'notice/notification_manager.html'
	context = {
		'notifications': notification_qs,
	}
	return render(request, template, context)

def add_notification(request):
	if request.method == 'POST':
		# initialise the form
		notification_form = NotificationForm(request.POST or None)
		if notification_form.is_valid():
			notification_form.save()
			msg = "\nNotification added successfully"
			return JsonResponse({'success': True, 'message': msg})
		else:
			msg = "\nForm is Not Valid" \
				  "please check your data and submit again"
			return JsonResponse({'success':False, 'message':msg})
	else:
		notification_form = NotificationForm()
		template = 'notice/add_notification.html'
		context = {
			'form':notification_form,
		}
		return JsonResponse({'html_form':render_to_string(template, context, request=request) })

def edit_notification(request, notice_id=None):
	if request.method == 'POST':
		notification_qs = get_object_or_404(NoticeBoard, pk=notice_id)
		form = NotificationForm(request.POST, instance=notification_qs)
		if form.is_valid():
			form.save()
			msg = "\nNotice updated Successful"
			return JsonResponse({'success':True, 'message':msg})
		else:
			msg = "\nUpdating Failed Check your Info and update again"
			return JsonResponse({'success':False, 'message':msg})
	else:
		# check if th user has Posted the notification id
		if notice_id is not None:
			notification_qs = get_object_or_404(NoticeBoard, pk=request.GET['post_id'])
			template = 'notice/edit_notification.html'
			notification_form = NotificationForm(instance=notification_qs)
			contest = {
				'notice': notification_qs,
				'form':notification_form,
			}
			return JsonResponse({'html_form':render_to_string(template, contest, request=request)})
		else:
			msg = '\nPlease select a notification first'
			return JsonResponse({'success':False, 'message': msg})
