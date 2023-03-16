from django.urls import path
from . import views


# the urls for our application
urlpatterns = [
    path('', views.ScanList.as_view()),
    # testing path to be used when testing new functions
    # path('testing/', views.testing, name='testing'),
]