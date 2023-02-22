from django.urls import path
from . import views


# the urls for our application
urlpatterns = [
    path('', views.main, name='main'),
    path('coordinator/', views.users, name='users'),
    path('coordinator/details/<int:id>', views.details, name='details'),
    # the testing path is the only url that we are actually working with
    # it uses the testing function created in views
    path('testing/', views.testing, name='testing'),
]