#!/usr/bin/python
import sys
import requests
import argparse
from infoblox_client import connector
from infoblox_client import objects
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

parser = argparse.ArgumentParser(
        description='Create a number of VMs in Google Compute Engine. Google Cloud SDK must be installed and configured (gcloud init) and google-api-python-client and infoblox-client Python libraries must be installed.')
parser.add_argument('name', nargs='+', help='List of FQDNs for VMs to delete separated by spaces')
args=parser.parse_args()

niosip = '10.60.27.4'
niosuser = 'admin'
niospw = 'infoblox'
project='mythic-brook-146218'
zone='us-west1-a'
name = args.name[0]

opts = {'host': niosip, 'username': niosuser, 'password': niospw}
conn = connector.Connector(opts)


def delete_instance(compute, project, zone, name):
	return compute.instances().delete(
	project=project,
	zone=zone,
	instance=name).execute()

print args.name

for name in args.name:
	splitname = name.split('.',1)
	hostname = splitname[0]
	domain = splitname[1]
# [START delete_instance]
	print(delete_instance(compute, project, zone, hostname))
	hr = objects.HostRecord.search(conn, name=name)
	objects.HostRecord.delete(hr)
