from django.contrib import admin

# Register your models here.
from .models import UVAClass, Profile

admin.site.register(UVAClass)
admin.site.register(Profile)