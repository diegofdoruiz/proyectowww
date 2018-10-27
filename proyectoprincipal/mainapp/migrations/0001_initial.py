# Generated by Django 2.1.2 on 2018-10-27 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mainapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pic', models.ImageField(blank=True, null=True, upload_to=mainapp.models.path_profile_image)),
                ('id_card', models.CharField(blank=True, max_length=20, unique=True)),
                ('telephone', models.CharField(blank=True, max_length=20)),
                ('active', models.CharField(choices=[('S', 'Si'), ('N', 'No')], default='S', max_length=300)),
            ],
            options={
                'permissions': (('es_cliente', 'Cliente'), ('es_proveedor', 'Proveedor'), ('es_gerente', 'Gerente'), ('es_administrador', 'Administrador'), ('es_cajero_general', 'Cajero General'), ('es_cajero_ie', 'Cajero de Importaciones y Exportaciones'), ('es_cajero_s', 'Cajero de Seguros'), ('es_cajero_d', 'Cajero de transacciones en Dólares'), ('es_cajero_vip', 'Cajero VIP')),
            },
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('permission', models.ManyToManyField(blank=True, to='auth.Permission')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='rol',
            field=models.ManyToManyField(blank=True, to='mainapp.Rol'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
