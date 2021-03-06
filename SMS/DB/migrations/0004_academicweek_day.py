# Generated by Django 2.2.5 on 2020-02-26 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DB', '0003_auto_20200226_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], max_length=1)),
            ],
            options={
                'ordering': ('day',),
            },
        ),
        migrations.CreateModel(
            name='AcademicWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.ManyToManyField(to='DB.Day')),
            ],
        ),
    ]
