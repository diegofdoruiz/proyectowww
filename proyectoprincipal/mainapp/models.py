from django.contrib.auth.models import User, Permission
from django.db import models
from django.utils.translation import gettext as _


class Rol(models.Model):
<<<<<<< HEAD
    name = models.CharField(max_length=20, null=False, blank=False)
=======
    name = models.CharField(max_length=20, null=False)
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f
    permission = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


# Función para crear ruta de las imágenes de perfil
def path_profile_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = 'profile'
    return "user/profile/{}/{}.{}".format(instance.user.id, new_filename, ext)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    pic = models.ImageField(blank=True, null=True, upload_to=path_profile_image)
    rol = models.ManyToManyField(Rol, blank=True)
    id_card = models.CharField(max_length=20, blank=True, unique=True)
    telephone = models.CharField(max_length=20, blank=True)

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

<<<<<<< HEAD
class Priority(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.CharField(max_length=512, null=False, blank=False)
    weight = models.IntegerField(null=False, blank=False)
    status = models.BooleanField(null=False)
    
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    
    def __str__(self):
        return self.name
        
class turn(models.Model):
    code = models.CharField(max_length=128, null=False, blank=False)
    service = models.CharField(max_length=512, null=False, blank=False)
    user_id = models.IntegerField(null=False, blank=False)
    status = models.BooleanField(null=False)
    
    def __str__(self):
        return self.code
=======
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f

'''
@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.profile.save()
'''

