from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import User
from datetime import datetime

#import the TenableIO class
from tenable.io import TenableIO

# import the Scan object model that is created in the models file
from .models import Scan

# instantiate tenable object
tio = TenableIO()

def main(request):
    context = {}
    template = loader.get_template('template.html')
    if request.method == "POST":
        scanName = request.POST.get('scan_name')
        description = request.POST.get('description')
        target = request.POST.get('target')
        target = target.split(", ")
        schedule = request.POST.get('schedule')
        date = datetime.now()
        Scan.objects.create(scanName=scanName, description=description, target=target, schedule=schedule, date=date)

        # logic for a quarterly scan, i.e. the only one we need to set an interval for
        if schedule == 'quarterly':
            # monthly is the value that tenable API accepts, so we change it back to monthly after grabbing from POST
            schedule = 'monthly'
            # set interval to 3 because 12 / 3 = 4 (aka quarterly)
            interval = 3
        else:
            # otherwise we set the interval to 1 so a scan will run as normal
            interval = 1

        # Grab the schedule for scan
        frequency = tio.scans.create_scan_schedule(
            enabled=True,
            frequency=schedule,
            interval= interval,
            weekdays=['MO'],
            starttime=datetime.now()
        )
        # Provision a scan with variable names
        # Still need to add description
        scan = tio.scans.create(
            name = scanName,
            targets = target,
            schedule_scan = frequency
        )
        tio.scans.launch(scan['id'])

    
    return HttpResponse(template.render(context, request))