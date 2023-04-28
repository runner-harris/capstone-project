from .models import Scan
from .serializers import ScanSerializer
from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Scan
from .tasks import download_scan
from rest_framework.response import Response
from django_q.tasks import async_task
import paramiko
from .api_clients import tio, dradis_api, accesskey, secretkey, api_token

#projects = dradis_api.get_all_projects()

ssh = paramiko.SSHClient()

# instantiate paramiko object
ssh = paramiko.SSHClient()

class ScanList(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Scan.objects.all()
    serializer_class = ScanSerializer

    def create_and_launch_scan(self, scan_name, targets, schedule, email):
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
            name=scan_name,
            targets=targets,
            schedule_scan=frequency
        )
        tio.scans.launch(scan['id'])

        async_task(download_scan, scan['id'], accesskey, secretkey, api_token, scan_name)

        #dradis_api.create_project(scan_name, scan['id'], 0, [], 'Vulnerability Scan Project Template v1')

    def post(self, request, *args, **kwargs):
        scan_name = request.data['scanName']
        targets = request.data['target'].split(", ")
        schedule = request.data['schedule']
        email = request.data['email']

        self.create_and_launch_scan(scan_name, targets, schedule, email)

        return Response({'message': 'Scan created and run successfully'})
 