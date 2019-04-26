from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Profile, Rol, Service, Location, Specialty



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

class ServiceListSerializer(ModelSerializer):
    class Meta:
        model = Service
        fields = [
            'id',
            'name',
            'description',
            'specialty',
            'status'
        ]

class LocationListSerializer(ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'id',
            'name'

        ]

class SpecialtyListSerializer(ModelSerializer):
    class Meta:
        model = Specialty
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