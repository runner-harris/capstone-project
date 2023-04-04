from .models import Scan
from .serializers import ScanSerializer
from datetime import datetime
import time
from rest_framework import generics
from .models import Scan
from rest_framework.response import Response
import requests
from .dradis import Dradis
api_token = '9bSuGEzizcoEsGezYCyX'
url = 'https://cofc-dradis.soteria.io/'
dradis_api = Dradis(api_token, url)
projects = dradis_api.get_all_projects()

import json
import os

from tenable.io import TenableIO

import asyncio
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

    async def download(self, scanid, tio):
        status = 'pending'
        while status[-2:] != 'ed':
            await asyncio.sleep(10)
            status = tio.scans.status(scanid)
            

        # if status == 'canceled' error handler ??

        # assuming status is 'completed':
        # download nessus file
        with open(str(scanid) + '.nessus', 'wb') as reportobj:
            results = tio.scans.export(scanid,fobj=reportobj)
        return


    # Define asynchronous function that sends the email. 
    # It will take an instance of the 'EmailMessage' class as an arg 
    # and use 'aiosmtplin' library to send email asynchronously.
    # this function could probably be written outside of views.py
    async def send_email_async(email_message):
        # Create an instance of the aiosmtplib.SMTP class
        smtp_client = aiosmtplib.SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT)

        # Connect to the SMTP server
        await smtp_client.connect()

        # Login to the SMTP server if authentication is required
        if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
            await smtp_client.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

        # Send the email
        await smtp_client.send_message(email_message)

        # Disconnect from the SMTP server
        await smtp_client.quit()


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

        #print("above")

        #comptest()
        #print("below")

        asyncio.run(self.download(scan['id'], tio))
        
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
        # Send email: 
        asyncio.run(send_email_async(email)) # this should wait to send till after 'download()' is done




        return Response({'message': 'Scan created and run successfully'})

