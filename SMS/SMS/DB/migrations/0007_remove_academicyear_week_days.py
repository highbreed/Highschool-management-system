# Generated by Django 2.2.5 on 2020-03-16 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0006_auto_20200226_1708'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='academicyear',
            name='week_days',
        ),
    ]
