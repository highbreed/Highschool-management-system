# Generated by Django 2.2.5 on 2020-04-21 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0023_auto_20200421_1547'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='period',
            unique_together={('name', 'sort_order', 'start_time', 'end_time')},
        ),
    ]
