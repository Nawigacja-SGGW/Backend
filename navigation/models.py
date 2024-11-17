from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from polymorphic.models import PolymorphicModel

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)

class Guide(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)

class Object(PolymorphicModel):
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True, related_name="objects")
    guide = models.ForeignKey(Guide, on_delete=models.SET_NULL, blank=True, null=True, related_name="objects")

    class Meta:
        unique_together = ('latitude', 'longitude')

class PointObject(Object):
    event_category = models.CharField(max_length=255)
    event_start = models.DateTimeField(null=True, blank=True)
    event_end = models.DateTimeField(null=True, blank=True)

class AreaObject(Object):
    number = models.IntegerField(null=True, blank=True)
    is_paid = models.BooleanField(null=True, blank=True)

class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    deans_office_number = models.CharField(max_length=255)
    area_objects = models.ManyToManyField(AreaObject, through="AreaObjectFaculty", related_name="faculties")

class AreaObjectFaculty(models.Model):
    area_object = models.ForeignKey(AreaObject, on_delete=models.CASCADE, related_name="faculty_associations")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="area_object_associations")
    floor = models.CharField(max_length=255, null=True, blank=True)

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
    room = models.CharField(max_length=255, null=True, blank=True)
    object = models.ForeignKey(AreaObject, on_delete=models.CASCADE, related_name="important_place")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Prosimy podać email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    distance_sum = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class UserObjectSearch(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_object_search")
    object_latitude = models.CharField(max_length=255)
    object_longitude = models.CharField(max_length=255)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="user_object_search")
    timestamp = models.DateTimeField()
    route_created_count = models.IntegerField()