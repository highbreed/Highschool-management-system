# Generated by Django 2.2.5 on 2020-04-22 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0016_departmentgraduationcredits'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='is_selectable',
            field=models.BooleanField(default=False, help_text='select if subject is optional'),
        ),
    ]
