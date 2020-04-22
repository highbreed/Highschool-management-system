# Generated by Django 2.2.5 on 2020-03-26 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0014_auto_20200324_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='markingperiod',
            name='grade_posting_begins',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='markingperiod',
            name='grade_posting_ends',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='markingperiod',
            name='graded',
            field=models.BooleanField(default=False, help_text='This will allow teachers and administrators to enter final grades for this marking period '),
        ),
    ]
