from django.urls import path
from django.contrib.auth import login

from . import views
urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
]