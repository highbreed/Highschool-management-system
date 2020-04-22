# Generated by Django 2.2.5 on 2020-03-16 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0006_auto_20200316_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolevent',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolevent',
            name='title',
            field=models.CharField(help_text='NB:  this is a system wide event service all events created will \nresults in system wide notification, \nFor personalised events go to noticeboard/Events', max_length=255),
        ),
    ]
