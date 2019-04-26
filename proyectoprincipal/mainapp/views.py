from django.shortcuts import redirect
from django.http import HttpResponse
from django.utils.html import escape
from django.contrib.auth.models import User, Permission, Group as Rol
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from .models import Profile, Service, Location, Specialty, Turn, LocationOnService
from django.contrib.auth.decorators import login_required
from .forms import UserForm, ProfileForm, CreateRolForm, ServiceForm, LocationForm, SpecialtyForm, LocationOnServiceForm
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
from django.http import JsonResponse
from datetime import datetime as lib_date
import datetime
from rolepermissions.roles import assign_role, clear_roles

from .forms import ComposeForm
from .models import Thread, ChatMessage

from .queue import Queue
########################### Usuarios ##########################

@login_required
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        return redirect('login/')

@login_required
@transaction.atomic
def register(request):
    user_form = UserForm(request.POST or None)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, request=None)
    if request.method == 'POST':
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()
            for g in request.POST.getlist('groups'):
                group = Rol.objects.get(pk=g)
                new_user.groups.add(group)
            profile = profile_form.save(commit=False)
            profile.user = new_user
            profile.save()
            # speciality_id = request.POST.get('specialty')
            # if speciality_id != '':
            #     # return HttpResponse(escape(repr(speciality_id)))
            #     specialty = get_object_or_404(Specialty, pk=speciality_id)
            #     print(specialty)
            #     added = profile.specialty.add(specialty)
            # return render(request, 'registration/confirmation.html', {'alert': ' User created has been created'})
            return redirect('/mainapp/users/')
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
            updated_user.groups.clear()
            for g in request.POST.getlist('groups'):
                group = Rol.objects.get(pk=g)
                updated_user.groups.add(group)
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
def roles(request, pk=None):
    #Informacion para la tabla
    request_from = request.GET.get('from', None)
    query = request.GET.get('search_text', None)
    if pk:
        rol_to_edit = get_object_or_404(Rol, pk=pk)
        form = CreateRolForm(instance=rol_to_edit)
    else:
        rol_to_edit = None
        form = CreateRolForm()
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
        rol_id = request.POST.get('rol_id', None)
        if rol_id:
            rol_to_edit = get_object_or_404(Rol, pk=pk)
            print(rol_to_edit)
            form = CreateRolForm(request.POST or None, instance=rol_to_edit)
        else:
            form = CreateRolForm(request.POST)

        if form.is_valid():
            rol = form.save()
            return redirect('/mainapp/roles')

        else:
            return render(request, 'users/create_rol.html', {'form': form, 'all_data': data})

    else:
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
    LocationOnService.objects.filter(user=request.user).update(status='4')
    form = LocationOnServiceForm()
    return render(request, 'turnos/atender_turnos.html',{'form':form})

def select_window(request):
    if request.POST:
        # Si ya alguien tiene la ventanilla abierta
        open_windows = LocationOnService.objects.exclude(status='4')
        same_open_window = open_windows.filter(window_id=request.POST.get('window'))
        if len(same_open_window) > 0:
            return JsonResponse({'success':False, 'error':'open'})

        LocationOnService.objects.filter(user=request.user).update(status='4')
        window_on_service, created = LocationOnService.objects.get_or_create(
            user_id=request.POST.get('user'),
            window_id=request.POST.get('window'),
        )
        if window_on_service or created == True:
            window_on_service.status = request.POST.get('status')
            queue = Queue()
            all_queue = queue.get_all_queue()
            window = Location.objects.get(id=request.POST.get('window'))
            return JsonResponse({'success':True, 'w_id':window.id, 'w_name':window.name, 'queue':all_queue})
    return JsonResponse({'success':False, 'error':''})

def change_status(request):
    user = request.GET.get('user_id')
    window = request.GET.get('window_id')
    status = request.GET.get('status')
    los = LocationOnService.objects.filter(user_id=user, window_id=window).update(status=status)
    if los:
        queue = Queue()
        all_queue = queue.get_all_queue()
        return JsonResponse({'success':True, 'queue':all_queue})    
    return JsonResponse({'success':False})

        

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
    return render(request, 'chat/room.html')

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
                        character = turn.service.name[0]+turn.service.name[1].upper()
                        if turns <= 0:
                            code = character+str(1)
                        else:
                            code = character+str(turns)
                        turn.code = code
                        turn.save()

                        queue = Queue()
                        all_queue = queue.get_all_queue()
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

def get_queue(request):
    queue = Queue()
    all_queue = queue.get_all_queue()
    return JsonResponse({'success':True, 'queue':all_queue})


def tests(request):
    queue = Queue()
    all_queue = queue.get_all_queue()
    window_on_service = LocationOnService.objects.get(user=request.user)
    window_on_service.status = '1'
    window_on_service.save()
    return render(request, 'tests/index.html', {
        'queue':all_queue,
        'status':window_on_service.status
        })

def borrar(request):
    queue = Queue()
    return HttpResponse(escape(repr(queue.get_all_queue())))

@transaction.atomic
def next_turn(request):
    queue = Queue()
    if request.GET:
        user_id = request.GET.get('user_id')
        window_id = request.GET.get('window_id')
        user = User.objects.get(pk=user_id)
        turn = queue.get_next(user)
        service_id = turn.service_id
        service = Service.objects.get(pk=service_id)
        client_id = turn.user1_id
        client= User.objects.get(pk=client_id);
        profile = Profile.objects.get(user=client)
        all_queue = queue.get_all_queue()
        window_on_service = LocationOnService.objects.get(user_id=user_id, window_id=window_id)
        window_on_service.status = '1'
        window_on_service.save()
        if turn:
            data = {'id' : turn.pk, 
                    'code':turn.code, 
                    'queue':all_queue,
                    'status':window_on_service.status,
                    'name': client.first_name,
                    'client_id':profile.id_card,
                    'service_name':service.name,
                    'window_id':window_on_service.window_id}
            return JsonResponse(data, safe=True)
        else:
            data = {'id' : '', 
                    'code':'', 
                    'queue':'',
                    'status':window_on_service.status}
            return JsonResponse(data, safe=True)

@transaction.atomic
def start_attend(request):
    if request.GET:
        user_id = request.GET.get('user_id')
        window_id = request.GET.get('window_id')
        queue = Queue()
        all_queue = queue.get_all_queue()
        window_on_service = LocationOnService.objects.get(user_id=user_id, window_id=window_id)
        turn_id = request.GET.get('turn_id')
        if turn_id:
            window_id = request.GET.get('window_id')
            turn = Turn.objects.get(pk=turn_id)
            window = Location.objects.get(pk=window_id)
            turn.status = '3'
            turn.start_attend = datetime.datetime.now()
            turn.user2 = request.user
            turn.window = window
            turn.save()
            window_on_service.status = '2'
            window_on_service.save()
            data = {
                'success': True,
                'queue': all_queue,
                'status':window_on_service.status
            }
            return JsonResponse(data)
        else:
            data = {
                'success': False,
                'queue': all_queue,
                'status':window_on_service.status
            }
            return JsonResponse(data)

@transaction.atomic
def end_attend(request):
    if request.GET:
        turn_id = request.GET.get('turn_id')
        user_id = request.GET.get('user_id')
        window_id = request.GET.get('window_id')
        turn = Turn.objects.get(pk=turn_id)
        turn.status = '4'
        turn.end_attend = datetime.datetime.now()
        turn.save()
        queue = Queue()
        all_queue = queue.get_all_queue()
        window_on_service = LocationOnService.objects.get(user_id=user_id, window_id=window_id)
        window_on_service.status = '1'
        window_on_service.save()
        data = {
            'success': True,
            'queue': all_queue,
            'status':window_on_service.status
        }
        return JsonResponse(data)
    else:
        data = {
            'success': False,
        }
        return JsonResponse(data)


def attending(request):
    return render(request, 'chat/index.html', {})


def reports(request):
    # LocationOnService.objects.filter(user=request.user).update(status='4')
    return render(request, 'reports/index.html')
