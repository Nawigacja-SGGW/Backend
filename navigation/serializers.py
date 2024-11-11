from rest_framework import serializers
from .models import (
    Address, Guide, Object, PointObject, AreaObject, Faculty, 
    AreaObjectFaculty, Institute, Entry, ImportantPlace, User, UserObjectSearch
)
from django.contrib.auth.models import User

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'postal_code', 'city']


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ['id', 'description']


class ObjectSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    guide = GuideSerializer()

    class Meta:
        model = Object
        fields = [
            'latitude', 'longitude', 'name', 'type', 'description', 
            'image_url', 'website', 'address', 'guide'
        ]


class PointObjectSerializer(serializers.ModelSerializer):
    object = ObjectSerializer()

    class Meta:
        model = PointObject
        fields = [
            'id', 'event_category', 'event_start', 'event_end', 
            'object_latitude', 'object_longitude', 'object'
        ]


class AreaObjectSerializer(serializers.ModelSerializer):
    object = ObjectSerializer()
    entry = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    important_place = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AreaObject
        fields = [
            'id', 'number', 'is_paid', 'object_latitude', 'object_longitude', 
            'object', 'entry', 'important_place'
        ]


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['id', 'name', 'deans_office_number']


class AreaObjectFacultySerializer(serializers.ModelSerializer):
    area_object = AreaObjectSerializer()
    faculty = FacultySerializer()

    class Meta:
        model = AreaObjectFaculty
        fields = ['area_object', 'faculty', 'floor']


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ['id', 'name']


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['object_latitude', 'object_longitude', 'object']


class ImportantPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantPlace
        fields = ['id', 'floor', 'room', 'object']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']



class UserObjectSearchSerializer(serializers.ModelSerializer):
    object = ObjectSerializer()

    class Meta:
        model = UserObjectSearch
        fields = [
            'user', 'object_latitude', 'object_longitude', 
            'object', 'timestamp', 'routeCreatedCount'
        ]
