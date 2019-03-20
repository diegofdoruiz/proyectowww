from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.html import escape
from django.contrib.auth.models import User, Permission
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from .models import Profile, Rol, Service, Location, Specialty, Turn
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm, CreateRolForm, ServiceForm, LocationForm, SpecialtyForm
from .serializers import UserListSerializer, ServiceListSerializer, LocationListSerializer, RolListSerializer, SpecialtyListSerializer
from .pagination import CustomPageNumberPagination
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate, login
from django.core import serializers

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView
from django.utils.safestring import mark_safe
import json
from datetime import datetime as lib_date
import datetime
from rolepermissions.roles import assign_role

from .forms import ComposeForm
from .models import Thread, ChatMessage

########################### Usuarios ##########################

def home(request):
    if request.user.is_authenticated:
        return redirect('home/')
    else:
        return redirect('login/')

@transaction.atomic
def register(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, request=None)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            for rr in request.POST.getlist('rol'):
                if rr == 'a':
                    assign_role(new_user, 'administrador')
                elif rr == 'b':
                    assign_role(new_user, 'cajero')
                else:
                    assign_role(new_user, 'cliente')

            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            for sp_id in request.POST.getlist('specialty'):
                specialty = get_object_or_404(Specialty, pk=sp_id)
                added = profile.specialty.add(specialty)
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
            rol = request.POST.get('rol')
            if rol == 'a':
                assign_role(updated_user, 'administrador')
            elif rol == 'b':
                assign_role(updated_user, 'cajero')
            else:
                assign_role(updated_user, 'cliente')
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

    if request.method == 'POST':
        form = CreateRolForm(request.POST)
        if form.is_valid():
            rol = form.save()
            for permission_id in request.POST.getlist('permissions'):
                permission = get_object_or_404(Permission, id=permission_id)
                rol.permission.add(permission)
            return redirect('/mainapp/roles')

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
def services(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    service_objects = Service.objects.all().order_by('id')
    if query:
        service_objects = service_objects.filter( Q(name__contains=query) | 
                                                    Q(description__contains=query) | 
                                                    Q(weight__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(service_objects, request)
    serializer = ServiceListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Crear la prioridad
    if request.method =='POST':   
        form = ServiceForm(request.POST) 
        if form.is_valid():    
            post = form.save(commit = False) 
            post.save()   
            return redirect('/mainapp/services')
              
        else: 
            return render(request, 'services/create.html', {'all_data': data, 'form': form})  
    else: 
        #formulario la creación de nueva prioridad 
        form = ServiceForm()
        return render(request, 'services/create.html', {'all_data': data, 'form': form})

@api_view(['POST'])
def edit_service(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    service_objects = Service.objects.all().order_by('id')
    if query:
        service_objects = service_objects.filter( Q(name__contains=query) | 
                                                    Q(description__contains=query) | 
                                                    Q(weight__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(service_objects, request)
    serializer = ServiceListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Editar la prioridad
    instance = get_object_or_404(Service, pk=request.POST.get('service_id'))
    #return HttpResponse(escape(repr(instance)))
    form = ServiceForm(request.POST, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            updated_service = form.save(commit=False)
            updated_service.save()
            form.save()
            return redirect('/mainapp/services')
        else:
            specialties = Specialty.objects.all().order_by('pk')
            return render(request, 'services/create.html', {
                'form1': form, 
                'request': request, 
                'all_data': data, 
                'specialties':specialties
                }
            )
    return redirect('/mainapp/services')

def destroy_service(request):
    if request.method == 'POST':
        service = get_object_or_404(Service, pk=request.POST.get('service_id'))
        service.delete()
        return redirect('/mainapp/services')

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
            updated_service = form.save(commit=False)
            updated_service.save()
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

###################### Servicios #######################
@api_view(['GET','POST'])
def specialties(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    specialty_objects = Specialty.objects.all().order_by('id')
    if query:
        specialty_objects = specialty_objects.filter( Q(name__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(specialty_objects, request)
    serializer = SpecialtyListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Crear la prioridad
    if request.method =='POST':   
        form = SpecialtyForm(request.POST) 
        if form.is_valid():    
            post = form.save(commit = False) 
            post.save()   
            return redirect('/mainapp/specialties')
              
        else: 
            return render(request, 'specialties/index.html', {'all_data': data, 'form': form})  
    else: 
        #formulario la creación de nueva prioridad 
        form = SpecialtyForm()
        return render(request, 'specialties/index.html', {'all_data': data, 'form': form})

@api_view(['POST'])
def edit_specialty(request):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    specialty_objects = Specialty.objects.all().order_by('id')
    if query:
        specialty_objects = specialty_objects.filter( Q(name__contains=query)).distinct().order_by('id')
    paginator = CustomPageNumberPagination()
    result_page = paginator.paginate_queryset(specialty_objects, request)
    serializer = SpecialtyListSerializer(result_page, many=True)
    if request_from:
        if request_from == 'search_input':
            return paginator.get_paginated_response(serializer.data)
    data = paginator.get_paginated_response(serializer.data)
    #Editar la prioridad    
    instance = get_object_or_404(Specialty, pk=request.POST.get('specialty_id'))
    form = SpecialtyForm(request.POST, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            updated_service = form.save(commit=False)
            updated_service.save()
            form.save()
            return redirect('/mainapp/specialties')
        else:
            return render(request, 'specialties/index.html', {'form1': form, 'request': request, 'all_data':data})
    return redirect('/mainapp/specialties')

def destroy_specialty(request):
    if request.method == 'POST':
        specialty = get_object_or_404(Specialty, pk=request.POST.get('specialty_id'))
        specialty.delete()
        return redirect('/mainapp/specialties')



@login_required
def atencion_clientes(request):
    return render(request, 'turnos/atender_turnos.html')

### Vistas para channels ###
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        self.success_url = './'+self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

@login_required
def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    if request.user.is_authenticated:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))})
    else:
        return render(request, 'chat/room.html', {
            'room_name_json': mark_safe(json.dumps(room_name))
        })

def pedir_turno(request, turn=''):
    if request.POST:
        step = request.POST.get('step')
        if step == '1':
            user_id = request.POST.get('id_card')
            if user_id:
                try:
                    profile = Profile.objects.get(id_card=user_id)
                    specialties = Specialty.objects.all().order_by('name')
                    if profile:
                        return render(request, 'turnos/pedir_turno.html', {
                            'step2':True, 
                            'error':'', 
                            'profile':profile,
                            'specialties':specialties})
                except Profile.DoesNotExist:
                    return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':'Usuario no encontrado'})
            else:
                return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':'Debe Completar el campo identificación'})
        elif step == '2':
            specialty_id = request.POST.get('specialty')
            profile_id = request.POST.get('profile_id')
            if specialty_id:
                try:
                    specialty = Specialty.objects.get(pk=specialty_id)
                    if specialty:
                        services = Service.objects.all().filter(specialty=specialty)
                        return render(request, 'turnos/pedir_turno.html', {
                            'step3':True, 
                            'profile_id':profile_id, 
                            'specialty': specialty,
                            'services': services
                            }
                        )
                except Profile.DoesNotExist:
                    return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':''})
            else:
                return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':''})
        elif step == '3':
            specialty_id = request.POST.get('specialty_id')
            profile_id = request.POST.get('profile_id')
            service_id = request.POST.get('service')
            if service_id:
                try:
                    service = Service.objects.get(pk=service_id)
                    if service:
                        profile = Profile.objects.get(pk=profile_id)
                        service = Service.objects.get(pk=service_id)
                        specialty = Specialty.objects.get(pk=specialty_id)
                        turn = Turn()
                        turn.status = '1'
                        turn.user1 = profile.user
                        turn.service = service
                        turn.specialty = specialty
                        turn.save()
                        # fecha para reiniciar los códigod de los turnos diáriamente
                        input_date = str(datetime.datetime.now().date())
                        from_date = lib_date.strptime(input_date, '%Y-%m-%d').date()
                        from_date = datetime.datetime.combine(from_date, datetime.time.min)
                        to_date = datetime.datetime.combine(from_date, datetime.time.max)
                        turns = Turn.objects.all().filter(specialty=specialty, service=service, created_at__range=(from_date, to_date)).count()
                        character = turn.specialty.name[0]+turn.service.name[0].upper()
                        if turns <= 0:
                            code = character+str(1)
                        else:
                            code = character+str(turns)
                        turn.code = code
                        turn.save()
                        return render(request, 'turnos/pedir_turno.html', {
                            'step4':True,
                            'turn':code,
                            }
                        )
                    else:
                        return render(request, 'turnos/pedir_turno.html', {'step3':True, 'error':'No existe la prioridad'})
                except Profile.DoesNotExist:
                    return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':''})
            else:
                return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':''})

    return render(request, 'turnos/pedir_turno.html', {'step1':True, 'error':''})

