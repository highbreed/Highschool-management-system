# Generated by Django 2.2.5 on 2020-02-23 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('DB', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoticeBoard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('date', models.DateField(auto_now_add=True)),
                ('description', models.TextField(max_length=700)),
                ('post_to_parents', models.BooleanField(blank=True, help_text='select to include parents as recipients \n NB: default all teachers are recipients ', null=True)),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posted_notice', to='DB.Teacher')),
            ],
        ),
    ]
