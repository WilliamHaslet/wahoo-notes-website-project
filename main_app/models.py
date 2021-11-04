import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    computing_id = models.CharField(max_length=30, default='NULL')
    year = models.IntegerField(default=0)
    def __str__(self):
        return f'{self.user.username} Profile'

class Class(models.Model):
    name = models.CharField(max_length=30)
    professor = models.CharField(max_length=30)
    time = models.CharField(max_length=30)
    semester = models.CharField(max_length=30)

class UVAClass(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    id_text = models.CharField(max_length=200)
    studentyr_text = models.CharField(max_length=200)
    classname_text = models.CharField(max_length=200)
    classtime_text = models.CharField(max_length=200)
    classinst_text = models.CharField(max_length=200)
    def __str__(self):
        return self.classname_text