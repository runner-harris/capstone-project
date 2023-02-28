from django.urls import path
from . import views


# the urls for our application
urlpatterns = [
    path('', views.main, name='main'),
    # testing path to be used when testing new functions
    # path('testing/', views.testing, name='testing'),
]