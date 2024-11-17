from django.contrib import admin
from .models import AreaObject, CustomUser, Object, PointObject

# Register your models here.
admin.site.register(AreaObject)
admin.site.register(CustomUser)
admin.site.register(Object)
admin.site.register(PointObject)