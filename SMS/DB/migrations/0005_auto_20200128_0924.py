# Generated by Django 2.2.5 on 2020-01-28 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0004_auto_20200128_0907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='academic_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='acasemic_tearm', to='DB.AcademicYear'),
        ),
    ]