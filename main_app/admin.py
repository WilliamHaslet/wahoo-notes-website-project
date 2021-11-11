from django.contrib import admin

# Register your models here.
from .models import Class, Profile, Assignment

admin.site.register(Class)
admin.site.register(Profile)
admin.site.register(Assignment)