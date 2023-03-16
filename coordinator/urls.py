from django.urls import path
from . import views


# the urls for our application
# ScanList is the class view we work with, declaring it .as_view() turns a class into a viewable resource
urlpatterns = [
    path('', views.ScanList.as_view()),
    # testing path to be used when testing new functions
    # path('testing/', views.testing, name='testing'),
]