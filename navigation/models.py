from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from polymorphic.models import PolymorphicModel

class Address(models.Model):
    id = models.AutoField(primary_key=True)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=6)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street}, {self.postal_code}, {self.city}"

class Guide(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.id} {self.description}"

class Object(PolymorphicModel):
    id = models.AutoField(primary_key=True)
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

    def __str__(self):
        return f"{self.name} {self.event_category} {self.event_start} {self.latitude[:8]}, {self.longitude[:8]}"

class AreaObject(Object):
    number = models.IntegerField(null=True, blank=True)
    is_paid = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.latitude[:8]}, {self.longitude[:8]}"

class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    deans_office_number = models.CharField(max_length=255)
    area_objects = models.ManyToManyField(AreaObject, through="AreaObjectFaculty", related_name="faculties")

    def __str__(self):
        return f"{self.name}"

class AreaObjectFaculty(models.Model):
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="faculty_associations")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="object_associations")
    floor = models.CharField(max_length=255, null=True, blank=True)
    

class Institute(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    object = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="institute")


class Entry(models.Model):
    id = models.AutoField(primary_key=True)
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="entry")
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)

    class Meta:
        unique_together = ('latitude', 'longitude')

    def __str__(self):
        return f"{self.id} {self.latitude} {self.longitude} {self.object_id}"


class ImportantPlace(models.Model):
    id = models.AutoField(primary_key=True)
    floor = models.IntegerField()
    room = models.CharField(max_length=255, null=True, blank=True)
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="important_place")

    def __str__(self):
        return f"{self.floor} {self.room} {self.object_id}"
        

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
    object_id = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="user_object_search")
    timestamp = models.DateTimeField()
    route_created_count = models.IntegerField()