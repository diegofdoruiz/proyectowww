from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.html import escape
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from .models import Profile, Rol, Priority, Location
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm, CreateRolForm, PriorityForm, LocationForm
from .serializers import UserListSerializer, PriorityListSerializer, LocationListSerializer, RolListSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.core import serializers

########################### Usuarios ##########################
<<<<<<< HEAD
=======
def home(request):
    if request.user.is_authenticated:
        return redirect('home/')
    else:
        return redirect('login/')

>>>>>>> 1a7444a01a1bdde3762c203017040539d0e509bd

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

@api_view(['GET',])
def users_list(request):
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    person_objects = User.objects.all().order_by('id')
    if query:
        person_objects = person_objects.filter(Q(username__contains=query) |
                                               Q(first_name__contains=query) |
                                               Q(last_name__contains=query) |
                                               Q(email__contains=query) |
                                               Q(is_active__contains=query) |
                                               Q(is_superuser__contains=query)).distinct().order_by('id')

    paginator = CustomPageNumberPagination()

    result_page = paginator.paginate_queryset(person_objects, request)
    serializer = UserListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)

    data = paginator.get_paginated_response(serializer.data)
    return render(request, 'users/index.html', {'all_data': data})


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


def user_delete(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.POST.get('user_id'))
        user.is_active = request.POST.get('option')
        user.save()
        return redirect('/mainapp/users')


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
            return redirect('/mainapp/edit_profile')
    return render(request, 'users/edit_profile.html', {'form': form, 'user_form': user_form})

<<<<<<< HEAD

class CreateRole(CreateView):
    model = Rol
    form_class = CreateRolForm
    template_name = 'users/create_rol.html'

    def form_valid(self, form):
        form.save()

        return redirect('/home')



def create_role(request):
=======
#################### Roles ##############################
@api_view(['GET','POST'])
def roles(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    rol_id = request.GET.get('rol_id', None)
    if rol_id:
        rol_to_edit = get_object_or_404(Rol, pk=rol_id)
    else:
        rol_to_edit = None
    rol_objects = Rol.objects.all().order_by('id')
    if query:
        rol_objects = rol_objects.filter(   Q(name__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(rol_objects, request)
    serializer = RolListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Almacenar rol
>>>>>>> 1a7444a01a1bdde3762c203017040539d0e509bd
    if request.method == 'POST':
        form = CreateRolForm(request.POST)
        if form.is_valid():
            form.save()
<<<<<<< HEAD
            return redirect('/')

=======
            return redirect('/mainapp/roles')
>>>>>>> 1a7444a01a1bdde3762c203017040539d0e509bd
        else:
            return render(request, 'users/create_rol.html', {'form': form, 'all_data': data})

    else:
        form = CreateRolForm()
        return render(request, 'users/create_rol.html', {'form': form, 'all_data': data, 'rol_to_edit': rol_to_edit})

def destroy_rol(request):
    if request.method == 'POST':
        rol = get_object_or_404(Rol, pk=request.POST.get('rol_id'))
        rol.delete()
        return redirect('/mainapp/roles')



###################### Prioridades #######################
@api_view(['GET','POST'])
def priorities(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    priority_objects = Priority.objects.all().order_by('id')
    if query:
        priority_objects = priority_objects.filter( Q(name__contains=query) | 
                                                    Q(description__contains=query) | 
                                                    Q(weight__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(priority_objects, request)
    serializer = PriorityListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Crear la prioridad
    if request.method =='POST':   
        form = PriorityForm(request.POST) 
        if form.is_valid():    
            post = form.save(commit = False) 
            post.save()   
            return redirect('/mainapp/priorities')
              
        else: 
            return render(request, 'priorities/create.html', {'all_data': data, 'form': form})  
    else: 
        #formulario la creación de nueva prioridad 
        form = PriorityForm()
        return render(request, 'priorities/create.html', {'all_data': data, 'form': form})

@api_view(['POST'])
def edit_priority(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    priority_objects = Priority.objects.all().order_by('id')
    if query:
        priority_objects = priority_objects.filter( Q(name__contains=query) | 
                                                    Q(description__contains=query) | 
                                                    Q(weight__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(priority_objects, request)
    serializer = PriorityListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Editar la prioridad
    instance = get_object_or_404(Priority, pk=request.POST.get('priority_id'))
    #return HttpResponse(escape(repr(instance)))
    form = PriorityForm(request.POST, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            updated_priority = form.save(commit=False)
            updated_priority.save()
            form.save()
            return redirect('/mainapp/priorities')
        else:
            return render(request, 'priorities/create.html', {'form1': form, 'request': request, 'all_data': data})
    return redirect('/mainapp/priorities')

def destroy_priority(request):
    if request.method == 'POST':
        priority = get_object_or_404(Priority, pk=request.POST.get('priority_id'))
        priority.delete()
        return redirect('/mainapp/priorities')

###################### Ubicaciones #######################
@api_view(['GET','POST'])
def locations(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    location_objects = Location.objects.all().order_by('id')
    if query:
        location_objects = location_objects.filter( Q(name__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(location_objects, request)
    serializer = LocationListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Crear la prioridad
    if request.method =='POST':   
        form = LocationForm(request.POST) 
        if form.is_valid():    
            post = form.save(commit = False) 
            post.save()   
            return redirect('/mainapp/locations')
              
        else: 
            return render(request, 'locations/index.html', {'all_data': data, 'form': form})  
    else: 
        #formulario la creación de nueva prioridad 
        form = LocationForm()
        return render(request, 'locations/index.html', {'all_data': data, 'form': form})

@api_view(['POST'])
def edit_location(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    location_objects = Location.objects.all().order_by('id')
    if query:
        location_objects = location_objects.filter( Q(name__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(location_objects, request)
    serializer = LocationListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Editar la prioridad
    instance = get_object_or_404(Location, pk=request.POST.get('location_id'))
    #return HttpResponse(escape(repr(instance)))
    form = LocationForm(request.POST, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            updated_priority = form.save(commit=False)
            updated_priority.save()
            form.save()
            return redirect('/mainapp/locations')
        else:
            return render(request, 'locations/index.html', {'form1': form, 'request': request, 'all_data':data})
    return redirect('/mainapp/locations')



def destroy_location(request):
    if request.method == 'POST':
        location = get_object_or_404(Location, pk=request.POST.get('location_id'))
        location.delete()
        return redirect('/mainapp/locations')


@login_required
def atencion_clientes(request):
    return render(request, 'turnos/atender_turnos.html')

