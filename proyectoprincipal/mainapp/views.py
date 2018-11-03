from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.db import transaction
from .models import Profile, Rol
from django.contrib.auth.decorators import login_required

from .forms import UserForm, ProfileForm, CreateRolForm


@transaction.atomic
def register(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, request=None)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            for rr in request.POST.getlist('rol'):
                rol = get_object_or_404(Rol, id=rr)
                profile.rol.add(rol)
            profile.save()
            return render(request, 'registration/confirmation.html', {'alert': ' User created has been created'})
        else:
            return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form})


def user_list(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'users/user_list.html', context)


def user_edit(request, pk):
    user_instance = get_object_or_404(User, pk=pk)
    profile_instance = get_object_or_404(Profile, user_id=user_instance.id)
    user_form = UserForm(request.POST or None, instance=user_instance)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile_instance)
    if request.method == 'POST':
        alert = 'User Update error'
        if user_form.is_valid() and profile_form.is_valid():
            old_pass = user_instance.password
            new_pass = request.POST.get('password1', '')
            updated_user = user_form.save(commit=False)
            if new_pass == '':
                updated_user.password = old_pass
            updated_user.save()
            profile_form.save()
            alert = 'User update successfull'
        return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form, 'alert': alert})
    return render(request, 'registration/signup.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def edit_profile(request):
    instance = get_object_or_404(Profile, user_id=request.user.id)
    user_form = UserForm(request.POST or None, instance=request.user, from_update_profile=True)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=instance, request=request)
    if request.method == 'POST':
        if form.is_valid() and user_form.is_valid():
            old_pass = request.user.password
            new_pass = request.POST.get('password1', '')
            updated_user = user_form.save(commit=False)
            if new_pass == '':
                updated_user.password = old_pass
            updated_user.save()
            form.save()
            return redirect('/')
    return render(request, 'users/edit_profile.html', {'form': form, 'user_form': user_form})


class CreateRole(CreateView):
    model = Rol
    form_class = CreateRolForm
    template_name = 'users/create_rol.html'

    def form_valid(self, form):
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




