from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Rol


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, required=True)
    first_name = forms.CharField(max_length=140, required=True)
    last_name = forms.CharField(max_length=140, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('pic', 'rol', 'id_card', 'telephone', 'active')


class CreateRolForm(forms.ModelForm):
    class Meta:
        model = Rol
        fields = ('name', 'permission')


