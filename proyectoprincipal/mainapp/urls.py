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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
