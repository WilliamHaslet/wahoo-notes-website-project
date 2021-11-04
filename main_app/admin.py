from django.contrib import admin

# Register your models here.
from .models import Class, Profile

admin.site.register(Class)
admin.site.register(Profile)