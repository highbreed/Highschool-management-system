# Generated by Django 2.2.5 on 2020-04-22 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0017_auto_20200422_0759'),
        ('schedule', '0025_auto_20200422_0631'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CoursePeriod',
            new_name='SubjectPeriod',
        ),
    ]
