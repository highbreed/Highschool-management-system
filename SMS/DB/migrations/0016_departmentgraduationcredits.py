# Generated by Django 2.2.5 on 2020-04-22 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0015_delete_departmentgraduationcredits'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentGraduationCredits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credits', models.DecimalField(decimal_places=2, max_digits=5, unique=True)),
                ('class_year', models.ForeignKey(help_text='Also applies to subsequent years unless a more recent requirement exists.', on_delete=django.db.models.deletion.CASCADE, to='DB.AcademicYear')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='DB.Department')),
            ],
            options={
                'unique_together': {('department', 'credits')},
            },
        ),
    ]
