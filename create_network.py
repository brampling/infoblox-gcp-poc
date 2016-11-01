#!/usr/bin/python

import niosutils
import gcloudutils
import sys
import requests
import json
import re
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
	description='Create a number of VMs in Google Compute Engine. Google Cloud SDK must be installed and configured (gcloud init) and google-api-python-client and infoblox-client Python libraries must be installed.',
	epilog='Example: \'./create_network.py newnet\' will create a new network called newnet')
parser.add_argument('name', nargs=1, help='Name of the new network')
args=parser.parse_args()
name = args.name[0]

niosip = '10.60.27.4'
niosuser = 'admin'
niospw = 'infoblox'
project='mythic-brook-146218'
zone='us-west1-a'

opts = {'host': niosip, 'username': niosuser, 'password': niospw}
conn = connector.Connector(opts)

wapiurl = niosutils.get_wapiurl(niosip, niosuser, niospw)

#iplist = niosutils.get_nextips(subnet, num, wapiurl, niosuser, niospw)

output = gcloudutils.create_network(compute, project, name)
print output
