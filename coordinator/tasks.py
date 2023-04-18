from tenable.io import TenableIO
from django_q.tasks import async_task
import time
import paramiko
import os
from .dradis import Dradis


def download_scan(scanid, accesskey, secretkey, api_token, scan_name):
        
        # instantiate tenable and paramiko object
        tio = TenableIO(accesskey, secretkey)
        ssh = paramiko.SSHClient()
        url = 'https://cofc-dradis.soteria.io'
        dradis_api = Dradis(api_token, url)

        status = 'pending'
        while status[-2:] != 'ed':
            time.sleep(10)
            status = tio.scans.status(scanid)

        # TODO if status == 'canceled' throw an exception?

        with open(str(scanid) + '.nessus', 'wb') as reportobj:
            print(str(scanid))
            results = tio.scans.export(scanid,fobj=reportobj)

        # TODO UNSAFE, FOR TESTING ONLY. FIND A WAY AROUND THIS
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # better way to handle this?
        ssh.connect(os.getenv('DRADIS_HOSTNAME'),username=os.getenv('DRADIS_USER'),key_filename='./id_rsa')
        sftp = ssh.open_sftp()

        #setting up paths for sftp/scp of nessus file to dradis instance
        localpath = './' + str(scanid) + '.nessus'
        remotepath = '/opt/dradispro/dradispro/current/' + str(scanid) + '.nessus'

        print("Dradis Host: " + os.getenv('DRADIS_HOSTNAME') + "\n Dradis User: " + os.getenv('DRADIS_USER') + "\n local path: " + localpath + "\n remote path: " + remotepath)

        # Create Dradis project using same scan name and id as tenable
        dradis_api.create_project(scan_name, 0, 1, [], 'Vulnerability Scan Project Template v1')
        #get project ID ... can race condition happen with ID's?
        projects = dradis_api.get_all_projects()
        dID = projects[0]['id']

        ## 1 is Soteria's word template, hope that's true on other machines too

        sftp.put(localpath, remotepath) # copy file to home directory of user in dradis instance

        cmd1 = "export PROJECT_ID=" + str(dID) + " ; export RAILS_ENV=production ; cd /opt/dradispro/dradispro/current/ ; export PATH=/opt/rbenv/shims:/opt/rbenv/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games ; bundle exec thor dradis:plugins:nessus:upload " + "./" + str(scanid) + ".nessus"
        #print(cmd1)
        stdin, stdout, stderr = ssh.exec_command(cmd1)
        #print(stdout.read())
        #print(stderr.read())

        time.sleep(15) # need a loop that checks status, will implement later  
        
        cmd2 = "export PROJECT_ID=" + str(dID) + " ; export RAILS_ENV=production ; cd /opt/dradispro/dradispro/current/ ; export PATH=/opt/rbenv/shims:/opt/rbenv/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games ; bundle exec thor dradis:pro:plugins:word:export --output=/tmp/" + str(dID) + ".docm --template=templates/reports/word/vulnerability_scan-Internalv0.19.docm"
        #print(cmd2)
        stdin, stdout, stderr = ssh.exec_command(cmd2)
        #print(stdout.read())
        #print(stderr.read())
        sftp.get("/tmp/" + str(dID) + ".docm", "./" + str(dID) + ".docm") 

        sftp.close()
        ssh.close()
        return