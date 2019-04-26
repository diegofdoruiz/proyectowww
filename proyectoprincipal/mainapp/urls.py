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
    path('roles/', views.roles, name='roles'),
    path('roles/edit/<pk>', views.roles, name='role_edit'),
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

    path('select_window/', views.select_window, name='select_window'),
    path('atencion_clientes/', views.atencion_clientes, name='atencion_clientes'),
    path('change_status/', views.change_status, name='change_status'),
    path('notification/', views.index, name='index'),
<<<<<<< HEAD
    url(r'^notification/(?P<room_name>[^/]+)/$', views.room, name='room'),

    #reports
    path('reports/', views.reports, name='reports'),
=======
    #url(r'^notification/(?P<room_name>[^/]+)/$', views.room, name='room'),
>>>>>>> a8b48b08a12795b15db6617aae44e265a41336b9

    # Pedir turno
    path('pedir_turno/', views.pedir_turno, name='pedir_turno'),
    path('get_queue/', views.get_queue, name='get_queue'),

    path('tests/', views.tests, name='tests'),
    path('next_turn/', views.next_turn, name='next_turn'),
    path('start_attend/', views.start_attend, name='start_attend'),
    path('end_attend/', views.end_attend, name='end_attend'),

    path('borrar/', views.borrar, name='borrar'),
    path('publicidad/', views.publicidad, name='publicidad'),
    path('destroy_publicidad/', views.destroy_publicidad, name='destroy_publicidad'),
    # Borrar Cola
    path('attending/', views.attending, name='attending'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
