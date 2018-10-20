from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from .models import Profile, Rol
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm, EditProfileForm, CreateRolForm


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


class EditProfileView(CreateView):
    model = Profile
    form_class = EditProfileForm
    template_name = 'users/edit_profile.html'

    def form_valid(self, form):
        form.save()
        return redirect('/')


# @login_required
# def edit_profile(request, pk):
#   if request.method == 'POST':
#        instance = get_object_or_404(Profile, pk=pk)
#        form = EditProfileForm(request.POST or None, request.FILES, instance=instance)
#        if form.is_valid():
#            form.save()
#            return redirect('/')
#    else:
#        instance = get_object_or_404(Profile, pk=pk)
#        form = EditProfileForm(instance=instance)
#        return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        instance = get_object_or_404(Profile, user_id=request.user.id)
        form = EditProfileForm(request.POST or None, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        instance = get_object_or_404(Profile, user_id=request.user.id)
        form = EditProfileForm(instance=instance)
        return render(request, 'users/edit_profile.html', {'form': form})


class CreateRole(CreateView):
    model = Rol
    form_class = CreateRolForm
    template_name = 'users/create_rol.html'

    def form_valid(self, form):
        '''
        En este parte, si el formulario es valido guardamos lo que se obtiene de él y usamos authenticate para que el usuario incie sesión luego de haberse registrado y lo redirigimos al index
        '''
        form.save()
        return redirect('/')


def create_role(request):
    if request.method == 'POST':
        form = CreateRolForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = CreateRolForm()
        return render(request, 'users/create_rol.html', {'form': form})





