# Generated by Django 2.2.5 on 2020-01-29 13:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0009_remove_studentclass_academic_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentclass',
            name='academic_year',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='DB.AcademicYear'),
            preserve_default=False,
        ),
    ]
