from .models import Scan
from .serializers import ScanSerializer
from datetime import datetime
from rest_framework import generics
from .models import Scan

import json
import os

from tenable.io import TenableIO

# load apikeys.json, located in coordinator folder (better way to do this?) 
apipath = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'apikeys.json')

with open(apipath) as keys:
    data = json.load(keys)

# load apikeys from apikeys.json
accesskey = data['Access']
secretkey = data['Secret']

# instantiate tenable object
tio = TenableIO(accesskey, secretkey)

# create a view of the create scan form
# this view shows input fields for all of our scan model instances
# this class is passed to our URLS.py file in the coordinator app so that it displays on the screen when called
# queryset is the Scan object from the data base -> we grab this information to be able to create and add more stuff to it
# we then use the serializer_class to create serializable fields that let us add data to the database
class ScanList(generics.CreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

# run_scan is a function that creates a scan and runs it
# we pass 'self' as an argument to get the current instances of the class
# request as an argument so we can request data from the server
# serializer takes that data (that is in JSON format) and pulls what we need to so we can create a scan with it
    def run_scan(self, request):
        serializer = ScanSerializer(data=request.data)
        target = serializer.data['target']
        target.split(", ")
        schedule = serializer.data['schedule']
        if schedule == 'quarterly':
            schedule = 'monthly'
            interval = 3
        else:
            interval = 1

        frequency = tio.scans.create_scan_schedule(
            enabled=True,
            frequency=schedule,
            interval=interval,
            weekdays=['MO'],
            starttime=datetime.now()
        )
        scan = tio.scans.create(
            name = serializer.data['scanName'],
            targets = target,
            schedule_scan = frequency
        )
        tio.scans.launch(scan['id'])

# def main(request):
#     context = {}
#     template = loader.get_template('template.html')
#     if request.method == "POST":
#         scanName = request.POST.get('scan_name')
#         description = request.POST.get('description')
#         target = request.POST.get('target')
#         target = target.split(", ")
#         schedule = request.POST.get('schedule')
#         date = datetime.now()
#         Scan.objects.create(scanName=scanName, description=description, target=target, schedule=schedule, date=date)

#         # logic for a quarterly scan, i.e. the only one we need to set an interval for
#         if schedule == 'quarterly':
#             # monthly is the value that tenable API accepts, so we change it back to monthly after grabbing from POST
#             schedule = 'monthly'
#             # set interval to 3 because 12 / 3 = 4 (aka quarterly)
#             interval = 3
#         else:
#             # otherwise we set the interval to 1 so a scan will run as normal
#             interval = 1

#         # Grab the schedule for scan
#         frequency = tio.scans.create_scan_schedule(
#             enabled=True,
#             frequency=schedule,
#             interval= interval,
#             weekdays=['MO'],
#             starttime=datetime.now()
#         )
#         # Provision a scan with variable names
#         # Still need to add description
#         scan = tio.scans.create(
#             name = scanName,
#             targets = target,
#             schedule_scan = frequency
#         )
#         tio.scans.launch(scan['id'])

    
#     return HttpResponse(template.render(context, request))