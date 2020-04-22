from django.db import models
# noinspection PyUnresolvedReferences
from DB.models import Teacher

# Create your models here.


class NoticeBoard(models.Model):

	# contains data for notifications

	title = models.CharField(max_length=150)
	date = models.DateField(auto_now_add=True)
	description = models.TextField(max_length=700)
	post_to_parents = models.BooleanField(blank=True, null=True, help_text="select to include parents as recipients \n NB: default all teachers are recipients ")
	author = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True, related_name='posted_notice')

	def __str__(self):
		return self.title

