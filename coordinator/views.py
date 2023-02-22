from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
import datetime

# import the Scan object model that is created in the models file
from .models import Scan

# commented out code was just for testing/playing aroun puposes
# users and details are functions I made for practicing django. 
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

# main brings us to the home page
def main(request):
    template = loader.get_template('main.html')
    return HttpResponse(template.render())



# the testing function is used for trying out new functions
# we will change this to a new name once we have it working how we want
# right now it creates a Scan object and stores that in a database
def testing(request):
    template = loader.get_template('template.html')
    scanName = request.POST.get('scan_name')
    description = request.POST.get('description')
    target = request.POST.get('target')
    schedule = request.POST.get('schedule')
    date = datetime.date.today()
    
    Scan.objects.create(scanName=scanName, description=description, target=target, schedule=schedule, date=date)
    context = {}
    return HttpResponse(template.render(context, request))