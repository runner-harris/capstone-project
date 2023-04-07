from tenable.io import TenableIO
from django_q.tasks import async_task
import time
from django.core.mail import send_mail


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


#def send_email_async(email_message):
    # Create an instance of the aiosmtplib.SMTP class
    #smtp_client = aiosmtplib.SMTP(hostname=settings.EMAIL_HOST, port=settings.EMAIL_PORT)

    # Connect to the SMTP server
    #await smtp_client.connect()

    # Login to the SMTP server if authentication is required
    #if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
    #    await smtp_client.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # Send the email
    #await smtp_client.send_message(email_message)

    # Disconnect from the SMTP server
    #await smtp_client.quit()




    # redoing, this function gets called later so just smack the sync code to send an email here, probably don't even need to worry about redis
    #set up variables

    #send_mail('subject', 'body', sender_email, user_email)
