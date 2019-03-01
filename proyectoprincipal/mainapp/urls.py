from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('user_delete/', views.user_delete, name='user_delete'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_role/', views.create_role, name='create_role'),
    #path('signup/', views.register, name='signup'),
    path('users/', views.users_list, name='users'),
<<<<<<< HEAD
    path('priorities/', views.priorities, name='priorities'),
    path('edit_priority/', views.edit_priority, name='edit_priority'),
    path('destroy_priority/', views.destroy_priority, name='destroy_priority'),
    path('locations/', views.locations, name='locations'),
    path('edit_location/', views.edit_location, name='edit_location'),
    path('destroy_location/', views.destroy_location, name='destroy_location'),
    path('atencion_clientes/', views.atencion_clientes, name='atencion_clientes'),
=======
>>>>>>> b781bbc5447e812b65f01e1b63d8aeebb665fe0f
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
