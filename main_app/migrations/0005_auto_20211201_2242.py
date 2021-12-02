# Generated by Django 3.2.8 on 2021-12-02 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20211201_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_class', to='main_app.class'),
        ),
        migrations.AlterField(
            model_name='document',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document_profile', to='main_app.profile'),
        ),
    ]
