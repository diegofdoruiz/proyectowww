from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Permission(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Rol(models.Model):
    name = models.CharField(max_length=20, null=False)
    permission = models.ManyToManyField(Permission, blank=True)

    def __str__(self):
        return self.name


# Función para crear ruta de las imágenes de perfil
def path_profile_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = 'profile'
    return "user/profile/{}/{}.{}".format(instance.user.id, new_filename, ext)


class Profile(models.Model):
    activeChoices = (('S', 'Si'), ('N', 'No'))
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    pic = models.ImageField(blank=True, null=True, upload_to=path_profile_image)
    rol = models.ManyToManyField(Rol, blank=True)
    id_card = models.CharField(max_length=20, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    active = models.CharField(max_length=300, null=False, blank=False, choices=activeChoices, default='S')

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def crear_usuario_perfil(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def guardar_usuario_perfil(sender, instance, **kwargs):
    instance.profile.save()