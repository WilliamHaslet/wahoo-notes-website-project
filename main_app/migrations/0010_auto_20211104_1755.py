# Generated by Django 3.2.7 on 2021-11-04 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_delete_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='name',
        ),
        migrations.RemoveField(
            model_name='class',
            name='time',
        ),
        migrations.AddField(
            model_name='class',
            name='code',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='class',
            name='department',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='class',
            name='end_time',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AddField(
            model_name='class',
            name='section',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='class',
            name='size',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='class',
            name='start_time',
            field=models.TimeField(default='00:00:00'),
        ),
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.IntegerField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='class',
            name='professor',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AlterField(
            model_name='class',
            name='semester',
            field=models.CharField(default='None', max_length=30),
        ),
    ]