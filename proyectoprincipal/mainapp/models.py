from django.contrib.auth.models import User, Permission
from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.db.models import Q


class Rol(models.Model):

    name = models.CharField(max_length=20, null=False, blank=False)

    permission = models.ManyToManyField(Permission, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Función para crear ruta de las imágenes de perfil
def path_profile_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = 'profile'
    return "user/profile/{}/{}.{}".format(instance.user.id, new_filename, ext)


class Profile(models.Model):
    MY_CHOICES = (
        ('a', 'administrador'),
        ('b', 'cajero'),
        ('c', 'cliente'),
    )
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    pic = models.ImageField(blank=True, null=True, upload_to=path_profile_image)
    # rol = models.ManyToManyField(Rol, blank=True)
    rol = models.CharField(max_length=1, choices=MY_CHOICES)
    id_card = models.CharField(max_length=20, blank=True, unique=True)
    telephone = models.CharField(max_length=20, blank=True)
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
        permissions = (
            ('es_cliente', _('Cliente')),
            ('es_proveedor', _('Proveedor')),
            ('es_gerente', _('Gerente')),
            ('es_administrador', _('Administrador')),
            ('es_cajero_general', _('Cajero General')),
            ('es_cajero_ie', _('Cajero de Importaciones y Exportaciones')),
            ('es_cajero_s', _('Cajero de Seguros')),
            ('es_cajero_d', _('Cajero de transacciones en Dólares')),
            ('es_cajero_vip', _('Cajero VIP')),
        )


class Priority(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)
    weight = models.IntegerField(null=False, blank=False)
    status = models.BooleanField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# servicios disponible para atención
class Service(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)
    status = models.BooleanField(null=False)
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
        ('2', 'attending'),
        ('3', 'canceled'),
    )
    code = models.CharField(max_length=128, null=True, blank=False, unique=True)
    status = models.CharField(max_length=1, choices=MY_CHOICES)
    window = models.CharField(max_length=2, null=True, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.code

# Ubicación en servicio
class LocationOnService(models.Model):
    MY_CHOICES = (
        ('1', 'free'),
        ('2', 'attending'),
    )
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


'''
@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.profile.save()
'''

