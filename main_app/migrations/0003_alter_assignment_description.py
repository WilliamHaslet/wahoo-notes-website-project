# Generated by Django 3.2.7 on 2021-11-18 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.CharField(default='', max_length=200),
        ),
    ]