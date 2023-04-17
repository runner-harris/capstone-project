from .models import Scan
from .serializers import ScanSerializer
from datetime import datetime
import time
from rest_framework import generics
from .models import Scan
from .tasks import download_scan
from rest_framework.response import Response
import requests
from .dradis import Dradis
from dotenv import load_dotenv
load_dotenv()
import json
import os
from django_q.tasks import async_task
from tenable.io import TenableIO
import paramiko # for ssh access
from django.core.mail import send_mail
from django.conf import settings # to get a variable for email

# load apikeys from apikeys.json
accesskey = os.getenv('TENABLE_ACCESS_KEY')
secretkey = os.getenv('TENABLE_SECRET_KEY')
api_token = os.getenv('DRADIS_API_KEY')

url = 'https://cofc-dradis.soteria.io'
dradis_api = Dradis(api_token, url)
projects = dradis_api.get_all_projects()

# instantiate tenable object
tio = TenableIO(accesskey, secretkey)

# instantiate paramiko object
ssh = paramiko.SSHClient()

class ScanList(generics.CreateAPIView):
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def post(self, request, *args, **kwargs):
        scan_name = request.data['scanName']
        targets = request.data['target'].split(", ")
        schedule = request.data['schedule']
        user_email = request.data['email']

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

        async_task(download_scan,scan['id'], accesskey, secretkey, api_token, scan_name)

        # TODO 
        dradis_api.create_project(scan_name, scan['id'], 0, [], 'Vulnerability Scan Project Template v1')
        # return Response({'message': 'Scan created and run successfully'})
    



        # Prepare email message to be sent:
        target = request.data['target'] # I'm getting the target data again here for readability reasons, as I intend to include the targets in the email
        email_message = f'Scan report for target {target} has finished downloading.' # not REALLY necessary, just thought it would be nice to see what the target is so you can tell what report it's talking about
        
        # adding in more variables so the email params aren't as hardcoded:
        email_subject = 'Report Downloaded'
        sender_email = settings.EMAIL_HOST_USER # gets sender's email from settings.py

        # Send email: 
        async_task(send_mail(email_subject, email_message, sender_email, [user_email])) # this should wait to send till after 'download()' is done
        

        return Response({'message': 'Scan created and run successfully'})







