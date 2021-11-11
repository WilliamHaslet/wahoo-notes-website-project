# Generated by Django 3.2.7 on 2021-11-11 23:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.IntegerField(default=0, primary_key=True, serialize=False)),
                ('subject', models.CharField(default='None', max_length=30)),
                ('code', models.CharField(default='None', max_length=30)),
                ('section', models.CharField(default='None', max_length=30)),
                ('name', models.CharField(default='None', max_length=30)),
                ('professor', models.CharField(default='None', max_length=30)),
                ('size', models.IntegerField(default=0)),
                ('day', models.CharField(default='None', max_length=30)),
                ('start_time', models.TimeField(default='00:00:00')),
                ('end_time', models.TimeField(default='00:00:00')),
                ('semester', models.CharField(default='None', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('computing_id', models.CharField(default='NULL', max_length=30)),
                ('year', models.IntegerField(default=0)),
                ('classes', models.ManyToManyField(related_name='profiles', to='main_app.Class')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NULL', max_length=30)),
                ('description', models.CharField(default='NULL', max_length=30)),
                ('points', models.IntegerField(default=0)),
                ('class_name', models.CharField(default='NULL', max_length=30)),
                ('release_date', models.CharField(default='NULL', max_length=30)),
                ('due_date', models.CharField(default='NULL', max_length=30)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='main_app.profile')),
            ],
        ),
    ]
