from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)

class Guide(models.Model):
    description = models.CharField(max_length=255)

class Object(models.Model):
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, related_name="objects")
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, null=True, related_name="objects")

class PointObject(models.Model):
    id = models.AutoField(primary_key=True)
    event_category = models.CharField(max_length=255)
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
    floor = models.CharField(max_length=255)

class Institute(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    object = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="institute")

class Entry(models.Model):
    object_latitude = models.IntegerField()
    object_longitude = models.IntegerField()
    object = models.ForeignKey(AreaObject, on_delete=models.CASCADE, related_name="entry")

class ImportantPlace(models.Model):
    id = models.AutoField(primary_key=True)
    floor = models.IntegerField()
    room = models.CharField(max_length=255)
    object = models.ForeignKey(AreaObject, on_delete=models.CASCADE, related_name="important_place")

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=128)

class UserObjectSearch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_object_search")
    object_latitude = models.CharField(max_length=255)
    object_longitude = models.CharField(max_length=255)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="user_object_search")
    timestamp = models.DateTimeField()
    routeCreatedCount = models.IntegerField()