# Generated by Django 2.2.5 on 2020-03-26 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0008_delete_schoolevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='short_name',
        ),
    ]
