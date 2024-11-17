from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import AreaObject, PointObject, CustomUser, Address, Guide, Entry, ImportantPlace


# Dodanie tablicy Entry do AreaObject
class EntryInline(admin.TabularInline):
    model = Entry
    extra = 1


# Dodanie tablicy ImportantPlace do AreaObject
class ImportantPlaceInline(admin.TabularInline):
    model = ImportantPlace
    extra = 1


# Dodanie AreaObject do panelu admina wraz z tablicami Entry i ImportantPlace
class AreaObjectAdmin(admin.ModelAdmin):
    inlines = [EntryInline, ImportantPlaceInline]


class UserAdmin(admin.ModelAdmin):
    model = CustomUser


admin.site.register(CustomUser, UserAdmin)
admin.site.register(AreaObject, AreaObjectAdmin)
admin.site.register(PointObject)

admin.site.register(Address)
admin.site.register(Guide)