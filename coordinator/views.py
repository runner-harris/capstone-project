from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
from .models import Scan

def users(request):
    myusers = User.objects.all().values()
    template = loader.get_template('all_users.html')
    context = {
        'myusers': myusers,
    }
    return HttpResponse(template.render(context, request))

def details(request, id):
    myuser = User.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'myuser': myuser,
    }
    return HttpResponse(template.render(context, request))

def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())

def testing(request):
    template = loader.get_template('template.html')
   # print(request.POST)
    
    scanName = request.POST.get('scan_name')
    description = request.POST.get('description')
    target = request.POST.get('target')
    print(scanName, description, target)
    Scan.objects.create(scanName = scanName, description = description, target=target)
    context = {}
    return HttpResponse(template.render(context, request))