from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Profile, Rol, Priority, Location, Service



class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'is_superuser'

        ]

class PriorityListSerializer(ModelSerializer):
    class Meta:
        model = Priority
        fields = [
            'id',
            'name',
            'description',
            'weight',
            'status'
        ]

class LocationListSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'name'

        ]

class ServiceListSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'description',
            'status'
        ]

class RolListSerializer(ModelSerializer):
    class Meta:
        model = Rol
        fields = [
            'id',
            'name'        

        ]