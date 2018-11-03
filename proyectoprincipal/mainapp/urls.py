from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('user_list/', views.user_list, name='user_list'),
    path('user_edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_role/', views.create_role, name='create_role'),
    path('signup/', views.register, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
