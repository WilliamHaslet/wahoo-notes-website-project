from django.contrib import admin

# Register your models here.
from .models import Class, Profile, Assignment, Document

admin.site.register(Class)
admin.site.register(Profile)
admin.site.register(Assignment)
admin.site.register(Document)