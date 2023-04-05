from tenable.io import TenableIO
from django_q.tasks import async_task
import time

def download_scan(scanid, accesskey, secretkey):

        tio = TenableIO(accesskey, secretkey)

        status = 'pending'
        while status[-2:] != 'ed':
            time.sleep(10)
            status = tio.scans.status(scanid)

        # if status == 'canceled' error handler ??

        # assuming status is 'completed':
        # download nessus file
        with open(str(scanid) + '.nessus', 'wb') as reportobj:
            print(id)
            results = tio.scans.export(scanid,fobj=reportobj)
