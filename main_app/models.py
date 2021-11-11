import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.

class Class(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    subject = models.CharField(max_length=30, default="None")
    code = models.CharField(max_length=30, default="None")
    section = models.CharField(max_length=30, default="None")
    name = models.CharField(max_length=30, default="None")
    professor = models.CharField(max_length=30, default="None")
    size = models.IntegerField(default=0)
    day = models.CharField(max_length=30, default="None")
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="00:00:00")
    semester = models.CharField(max_length=30, default="None")
    def __str__(self):
        return f"{self.subject} {self.code}, section {self.section}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    computing_id = models.CharField(max_length=30, default='NULL')
    year = models.IntegerField(default=0)
    classes = models.ManyToManyField('Class', related_name='profiles')
    def __str__(self):
        return f'{self.user.username} Profile'

class Assignment(models.Model):
    id = models.BigIntegerField(primary_key = True)
    profile = models.ForeignKey(Profile, related_name='assignments', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30, default='NULL')
    description = models.CharField(max_length=30, default='NULL')
    points = models.IntegerField(default=0)
    class_name = models.CharField(max_length=30, default='NULL')
    release_date = models.CharField(max_length=30, default='NULL')
    due_date = models.CharField(max_length=30, default='NULL')
    def __str__(self):
        return f'{self.name}'

class Document(models.Model):
    title = models.CharField(max_length=50, blank=True)
    document = models.FileField(upload_to='documents/')
