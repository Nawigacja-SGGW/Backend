from django.contrib import admin
from .models import Object, CustomUser

# Register your models here.
admin.site.register(Object)

admin.site.register(CustomUser)