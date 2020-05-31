from django import forms

from .models import NoticeBoard


class NotificationForm(forms.ModelForm):
	class Meta:
		model = NoticeBoard
		fields = "__all__"
		exclude = [
			'author',
		]