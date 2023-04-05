from .models import Scan
from .serializers import ScanSerializer
from datetime import datetime
import time
from rest_framework import generics
from .models import Scan
from .tasks import download_scan, send_email_async
from rest_framework.response import Response
import requests
from .dradis import Dradis
api_token = '9bSuGEzizcoEsGezYCyX'
url = 'https://cofc-dradis.soteria.io'
dradis_api = Dradis(api_token, url)
projects = dradis_api.get_all_projects()

from django_q.tasks import async_task

import json
import os

from tenable.io import TenableIO


# some more imports for email stuff:
import aiosmtplib
from django.core.mail import EmailMessage
from django.conf import settings


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

    # Define asynchronous function that sends the email. 
    # It will take an instance of the 'EmailMessage' class as an arg 
    # and use 'aiosmtplin' library to send email asynchronously.
    # this function could probably be written outside of views.py


    def post(self, request, *args, **kwargs):
        scan_name = request.data['scanName']
        targets = request.data['target'].split(", ")
        schedule = request.data['schedule']
        user_email = request.data['userEmail'].split(", ")

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
            name = scan_name,
            targets = targets,
            schedule_scan = frequency
        )
        tio.scans.launch(scan['id'])

        async_task(download_scan,scan['id'],accesskey,secretkey)


        # TODO 
        dradis_api.create_project(scan_name, 42, 0, [], 'Vulnerability Scan Project Template v1')
    
        # Prepare email message to be sent:
        target = request.data['target'] # I'm getting the target data again here for readability reasons, as I intend to include the targets in the email
        email_message = f'Scan report for target {target} has finished downloading.' # not REALLY necessary, just thought it would be nice to see what the target is so you can tell what report it's talking about
        email = EmailMessage(
            # 'Subject here', 'Here is the message', 'from@example.com', ['to@example.com'], reply_to=['another@example.com'], headers={'Message-ID': 'foo'}, # example one from online, i'm modifying this for our own but leaving this in case i mess it up/for reference.
            'Report Downloaded', # subject
            email_message, # email body
            '2023socapstone@gmail.com', # sender's email, I created a throwaway email for this
            [user_email], # recipient's address(es)
            # may wanna figure out the headers part, helps the email from being recieved as spam. But its something else to figure out and apparently it isn't necessary
        )

        # send_email_async moved to tasks.py
        # Send email: 
        # call async_task function. first arg is string name of function, following args are same as your function
        async_task(send_email_async,email) # this should wait to send till after 'download()' is done
        return Response({'message': 'Scan created and run successfully'})


