# Generated by Django 3.2.7 on 2021-11-04 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20211104_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='name',
            field=models.CharField(default='None', max_length=30),
        ),
    ]