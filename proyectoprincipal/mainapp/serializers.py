from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
<<<<<<< HEAD
from .models import Profile, Rol, Priority, Location
=======
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f


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
<<<<<<< HEAD
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
=======
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f
        ]