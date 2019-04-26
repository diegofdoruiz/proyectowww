from django.contrib.auth.models import User, Permission
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Q

# Función para crear ruta de las imágenes de perfil
def path_profile_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = 'profile'
    return "user/profile/{}/{}.{}".format(instance.user.id, new_filename, ext)

# servicios disponible para atención
class Specialty(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)
    status = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    pic = models.ImageField(blank=True, null=True, upload_to=path_profile_image)
    id_card = models.CharField(max_length=20, blank=True, unique=True)
    telephone = models.CharField(max_length=20, blank=True)
    specialty = models.ForeignKey(Specialty, blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.id:
            super(Profile, self).save(*args, **kwargs)
        # process self.parent_subject (should be called ...subjects, semantically)
        super(Profile, self).save(*args, **kwargs)

    class Meta:
        permissions = ()

class Service(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)
    status = models.BooleanField(null=False)
    specialty = models.ForeignKey(Specialty, related_name='specialty_r', null=False, blank=False, on_delete=models.CASCADE) # un servicio pertenece a una especialidad y una esp tien muchos ...
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# pueden ser las ventanillas
class Location(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Turno que llega    
class Turn(models.Model):
    MY_CHOICES = (
        ('1', 'waiting'),
        ('2', 'calling'),
        ('3', 'onservice'),
        ('4', 'attended'),
        ('5', 'canceled'),
    )
    code = models.CharField(max_length=128, null=True, blank=False, unique=True)
    status = models.CharField(max_length=1, choices=MY_CHOICES)
    user1 = models.ForeignKey(User, null=True, related_name='user_client', on_delete=models.SET_NULL)
    specialty = models.ForeignKey(Specialty, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    #Durante y después de la atención
    user2 = models.ForeignKey(User, null=True, related_name='user_employee', on_delete=models.SET_NULL)
    window = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL)
    start_attend = models.DateTimeField(null=True)
    end_attend = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

# Ubicación en servicio
class LocationOnService(models.Model):
    MY_CHOICES = (
        ('1', 'libre'),
        ('2', 'atendiendo'),
        ('3', 'pausado'),
        ('4', 'cerrado')
    )
    window = models.ForeignKey(Location, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=MY_CHOICES)

### Models for channels ###
class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False

class Thread(models.Model):
    first        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_first')
    second       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_thread_second')
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    
    objects      = ThreadManager()

    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False


class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='sender', on_delete=models.CASCADE)
    message     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

#Imagenes de publicidad
def path_publicity_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = 'publicity'
    return "user/publicity/{}/{}.{}".format(instance.nombre, new_filename, ext)

class Publicidad(models.Model):
    nombre = models.CharField(max_length=128, null=False, blank=False)
    imagen = models.ImageField(blank=True, null=True, upload_to=path_publicity_image)
    
    def __str__(self):
        return self.nombre