from .models import Profile, Service, Location, Specialty, Turn, LocationOnService
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
import json
from django.db import transaction


class Queue():
    # Usuarios de tipo cajeros, no se necesitan
    users = User.objects.filter(groups__name='Cajero').order_by('pk')
    # Ventanillas que están libres
    windows_on_service = LocationOnService.objects.all().filter(status=1)
    #Turnos esperando la atención, ordenados por hora de legada
    turns = Turn.objects.all().filter(status=1).order_by()

    def get_user_services(self, user):
        specialty =  user.profile.specialty
        if specialty:
            services = Service.objects.all().filter(specialty=specialty)
            return services
        else:
            return {}


    # retorna el id del siguiente turno que debe atender un usuario
    def get_fisrt_turn_pk(self, user):
        services = self.get_user_services(user)
        first = None
        # Turnos correspondientes a los servicios propios en orden de llegada
        turns_of_service = Turn.objects.all().filter(service__in=services, status='1').order_by('created_at')
        if turns_of_service:
            return turns_of_service.first().pk

        # Otros turnos en orden de llegada
        other_turns = Turn.objects.all().filter(status='1').exclude(service__in=services).order_by('created_at')
        if other_turns:
            return other_turns.first().pk
        return first

    # Proceso crítico, el cual debe estar en lo posible preparado para la concurrencia.
    # Retorna un turno, si la respuesta es un turno
    # es porque el turno estaba disponible y le cambió el estado a '2' : 'calling',
    # si la respuesta es None es porque debe seguir buscando un turno disponible
    @transaction.atomic
    def get_next(self, user):
        pk = self.get_fisrt_turn_pk(user)
        if pk:
            with transaction.atomic():
                turn = (
                    Turn.objects
                    .select_for_update()
                    .get(pk=pk)
                )
                if turn.status == '1':
                    turn.status = '2';
                    turn.save()
                    return turn
                else:
                    return None
        else:
            return None

    # Construir la cola para un usuario específico
    def build_queue_for_user(self, user):
        services = self.get_user_services(user)
        turns = {}
        cont = 1
        # Turnos correspondientes a los servicios propios en orden de llegada
        turns_of_service = Turn.objects.all().filter(service__in=services, status=1).order_by('created_at')
        for turn_of_service in turns_of_service:
            #turns.append(turn_of_service.code)
            turns[cont] = turn_of_service.code
            cont = cont + 1

        # Otros turnos en orden de llegada
        other_turns = Turn.objects.all().filter(status=1).exclude(service__in=services).order_by('created_at')
        for other_turn in other_turns:
            #turns.append(other_turn.code)
            turns[cont] = other_turn.code
            cont = cont + 1

        return turns

    def get_all_queue(self):
        window_detail = {}
        windows_detail = {}
        windows_on_service = LocationOnService.objects.all().filter(status=1)
        for window in windows_on_service:
            window_detail['turns'] = self.build_queue_for_user(window.user)
            windows_detail[window.user.pk] = window_detail 
            window = None
            window_detail = {}
        return windows_detail

