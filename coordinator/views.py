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
api_token = '9bSuGEzizcoEsGezYCyX'
url = 'https://cofc-dradis.soteria.io/'
dradis_api = Dradis(api_token, url)
projects = dradis_api.get_all_projects()

from django_q.tasks import async_task

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

    def post(self, request, *args, **kwargs):
        scan_name = request.data['scanName']
        targets = request.data['target'].split(", ")
        schedule = request.data['schedule']

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

        #download_scan(scan['id'],accesskey,secretkey)
        async_task(download_scan,scan['id'],accesskey,secretkey)

        return Response({'message': 'Scan created and run successfully'})

    

        ## hey

        # dradis_url = 'https://cofc-dradis.soteria.io/'
        # dradis_token = '9bSuGEzizcoEsGezYCyX'
        # dradis_project_id = '2'
        # dradis_upload_url = f'{dradis_url}/api/v0/projects/{dradis_project_id}/uploads'
        # headers = {'Authorization': f'Token {dradis_token}'}
        # files = {'file': ('scan_results.nessus', results, 'application/octet-stream')}
        # response = requests.post(dradis_upload_url, headers=headers, files=files)
        # upload_id = response.json()['id']

        # dradis_library_id = '488'
        # dradis_run_url = f'{dradis_url}/api/v0/projects/{dradis_project_id}/issues/{dradis_library_id}/run'
        # data = {'upload_id': upload_id}
        # response = requests.post(dradis_run_url, headers=headers, data=data)

        

