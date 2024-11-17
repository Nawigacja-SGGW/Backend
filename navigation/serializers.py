from rest_framework import serializers
from .models import (
    Address, Guide, Object, PointObject, AreaObject, Faculty, 
    AreaObjectFaculty, Institute, Entry, ImportantPlace, CustomUser, UserObjectSearch
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


class PointObjectSerializer(ObjectSerializer):

    class Meta:
        model = PointObject
        fields = [
            'latitude', 'longitude', 'name', 'type', 'description', 
            'image_url', 'website', 'address', 'guide', 'event_category',
            'event_start', 'event_end'
        ]


class AreaObjectSerializer(ObjectSerializer):
    entry = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    important_place = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AreaObject
        fields = [
            'latitude', 'longitude', 'name', 'type', 'description', 
            'image_url', 'website', 'address', 'guide', 'number',
            'is_paid', 'entry', 'important_place'
        ]


class ObjectDynamicSerializer(serializers.Serializer):
    
    def to_representation(self, instance):
        if isinstance(instance, AreaObject):
            serializer = AreaObjectSerializer(instance)
        elif isinstance(instance, PointObject):
            serializer = PointObjectSerializer(instance)
        else:
            raise ValueError("Unsupported instance type")
        return serializer.data


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
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserObjectSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObjectSearch
        fields = [
            'user', 'object_latitude', 'object_longitude', 'timestamp', 'route_created_count'
        ]


class UserObjectSearchExtendedSerializer(serializers.ModelSerializer):
    object = ObjectSerializer(read_only=True)

    class Meta:
        model = UserObjectSearch
        fields = [
            'user', 'object_latitude', 'object_longitude', 'object', 'timestamp', 'route_created_count'
        ]
    
    def create(self, validated_data):
        latitude = validated_data.pop('object_latitude')
        longitude = validated_data.pop('object_longitude')

        try:
            obj = Object.objects.get(latitude=latitude, longitude=longitude)
        except Object.DoesNotExist:
            raise serializers.ValidationError("Object with the specified latitude and longitude does not exist.")
        
        user_object_search = UserObjectSearch.objects.create(
            object=obj,
            object_latitude=latitude,
            object_longitude=longitude,
            **validated_data
        )

        return user_object_search


class UserExtendedSerializer(serializers.ModelSerializer):    
    user_object_search = UserObjectSearchSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'distance_sum', 'user_object_search']
        extra_kwargs = {'password': {'write_only': True}}