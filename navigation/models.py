from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)

class Object(models.Model):
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="objects")

class PointObject(models.Model):
    id = models.AutoField(primary_key=True)
    event_start = models.DateTimeField(null=True)
    event_end = models.DateTimeField(null=True)
    object_latitude = models.CharField(max_length=255)
    object_longitude = models.CharField(max_length=255)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="point_objects")

class AreaObject(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    is_paid = models.BooleanField()
    object_latitude = models.CharField(max_length=255)
    object_longitude = models.CharField(max_length=255)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="area_objects")

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    deans_office_number = models.CharField(max_length=255)
    area_objects = models.ManyToManyField(AreaObject, through="AreaObjectFaculty", related_name="faculties")

class AreaObjectFaculty(models.Model):
    area_object = models.ForeignKey(AreaObject, on_delete=models.CASCADE, related_name="faculty_associations")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="area_object_associations")
    floor = models.IntegerField()
