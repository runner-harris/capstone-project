from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('coordinator/', views.users, name='users'),
    path('coordinator/details/<int:id>', views.details, name='details'),
    path('testing/', views.testing, name='testing'),
]