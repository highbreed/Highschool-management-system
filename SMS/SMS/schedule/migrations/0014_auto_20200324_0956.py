# Generated by Django 2.2.5 on 2020-03-24 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0013_auto_20200324_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolevent',
            name='end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='schoolevent',
            name='start',
            field=models.DateTimeField(),
        ),
    ]
