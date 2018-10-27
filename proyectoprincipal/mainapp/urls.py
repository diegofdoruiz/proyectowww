from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('signup_alternative/', views.SignUpViewAlternative.as_view(), name='signup_alternative'),
    # path('editprofile/<int:pk>/', views.edit_profile, name='edit_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('create_role/', views.create_role, name='create_role'),
    path('signup/', views.signup, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
