# Generated by Django 2.2.5 on 2020-03-28 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0009_remove_subject_short_name'),
        ('schedule', '0017_auto_20200328_1550'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='markingperiod',
            unique_together={('name', 'academic_year', 'start_date', 'end_date', 'sort_order')},
        ),
    ]
