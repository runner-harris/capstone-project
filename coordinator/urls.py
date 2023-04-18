from django.urls import path
from . import views


urlpatterns = [
    path('scan/', views.ScanList.as_view(), name='scan-list'),
    ]