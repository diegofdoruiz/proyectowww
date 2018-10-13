from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView

from django.views.generic import CreateView
from .models import Profile

from .forms import SignUpForm


class SignUpView(CreateView):
    model = Profile
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        '''
        En este parte, si el formulario es valido guardamos lo que se obtiene de él y usamos authenticate para que el usuario incie sesión luego de haberse registrado y lo redirigimos al index
        '''
        form.save()
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        usuario = authenticate(username=usuario, password=password)
        login(self.request, usuario)
        return redirect('/')

