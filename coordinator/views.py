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
        email = request.data['email']

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

        return Response({'message': 'Scan created and run successfully'})
    



