from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views

# app_name = 'mainapp'
urlpatterns = [
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_delete/', views.user_delete, name='user_delete'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('roles', views.roles, name='roles'),
    path('destroy_rol/', views.destroy_rol, name='destroy_rol'),
    #path('signup/', views.register, name='signup'),
    path('users/', views.users_list, name='users'),
    
    path('services/', views.services, name='services'),
    path('edit_service/', views.edit_service, name='edit_service'),
    path('destroy_service/', views.destroy_service, name='destroy_service'),
    
    path('locations/', views.locations, name='locations'),
    path('edit_location/', views.edit_location, name='edit_location'),
    path('destroy_location/', views.destroy_location, name='destroy_location'),

    path('specialties/', views.specialties, name='specialties'),
    path('edit_specialty/', views.edit_specialty, name='edit_specialty'),
    path('destroy_specialty/', views.destroy_specialty, name='destroy_specialty'),

    path('atencion_clientes/', views.atencion_clientes, name='atencion_clientes'),
    # re_path(r"^(?P<username>[\w.@+-]+)", views.ThreadView.as_view()),
    #url(r'^$', views.index, name='index'),
    path('notification/', views.index, name='index'),
    url(r'^notification/(?P<room_name>[^/]+)/$', views.room, name='room'),

    # Pedir turno
    path('pedir_turno/', views.pedir_turno, name='pedir_turno'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
