from rest_framework import serializers
from .models import (
    Address, Guide, Object, PointObject, AreaObject, Faculty, 
    AreaObjectFaculty, Institute, Entry, ImportantPlace, CustomUser, UserObjectSearch
)
from django.contrib.auth.models import User

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'postal_code', 'city', 'city_eng']


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ['id', 'description', 'description_eng']


class ObjectSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    guide = GuideSerializer()

    class Meta:
        model = Object
        fields = [
            'id', 'latitude', 'longitude', 'name', 'name_eng', 'type', 'description', 'description_eng',
            'image_url', 'website', 'address', 'guide'
        ]


class PointObjectSerializer(ObjectSerializer):

    class Meta:
        model = PointObject
        fields = [
            'id', 'latitude', 'longitude', 'name', 'type', 'description',
            'image_url', 'website', 'address', 'guide', 'event_category',
            'event_start', 'event_end'
        ]


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'latitude', 'longitude']


class AreaObjectSerializer(ObjectSerializer):
    entry = EntrySerializer(many=True, read_only=True)
    important_place = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = AreaObject
        fields = [
            'id', 'latitude', 'longitude', 'name', 'type', 'description',
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
        fields = ['id', 'name', 'name_eng', 'deans_office_number']


class AreaObjectFacultySerializer(serializers.ModelSerializer):
    object_id = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    faculty = FacultySerializer()

    class Meta:
        model = AreaObjectFaculty
        fields = ['object_id', 'faculty', 'floor']


class InstituteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institute
        fields = ['id', 'name', 'name_eng']



class ImportantPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportantPlace
        fields = ['id', 'floor', 'room', 'object_id']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class UserObjectSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObjectSearch
        fields = [
            'object_id', 'timestamp', 'route_created_count'
        ]


class UserObjectSearchExtendedSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObjectSearch
        fields = [
            'user', 'object_id', 'timestamp', 'route_created_count'
        ]

    def create(self, validated_data):
        user_object_search = UserObjectSearch.objects.create(**validated_data)

        return user_object_search


class UserExtendedSerializer(serializers.ModelSerializer):    
    user_object_search = UserObjectSearchSerializer(many=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'distance_sum', 'user_object_search']
        extra_kwargs = {'password': {'write_only': True}}