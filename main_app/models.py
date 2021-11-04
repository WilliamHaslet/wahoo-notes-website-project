import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Class(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    department = models.CharField(max_length=30, default="None")
    code = models.CharField(max_length=30, default="None")
    section = models.CharField(max_length=30, default="None")
    name = models.CharField(max_length=30, default="None")
    professor = models.CharField(max_length=30, default="None")
    size = models.IntegerField(default=0)
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")
    semester = models.CharField(max_length=30, default="None")
    def __str__(self):
        return f"{self.department} {self.code}, section {self.section}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    computing_id = models.CharField(max_length=30, default='NULL')
    year = models.IntegerField(default=0)
    classes = models.ManyToManyField('Class', related_name='profiles')
    def __str__(self):
        return f'{self.user.username} Profile'