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
parser.add_argument('parent', nargs=1, help='Name of the parent network')
parser.add_argument('name', nargs=1, help='Name of the new subnet')
parser.add_argument('addr', nargs=1, help='Network range of parent Infoblox network container')
parser.add_argument('cidr', nargs=1, help='CIDR prefix for the new subnet')
args=parser.parse_args()
parent = args.parent[0]
name = args.name[0]
addr = args.addr[0]
cidr = args.cidr[0]

niosip = '10.60.27.4'
niosuser = 'admin'
niospw = 'infoblox'
project='mythic-brook-146218'
zone='us-west1-a'
splitzone = zone.split('-',2)
region = splitzone[0] + '-' + splitzone[1]

opts = {'host': niosip, 'username': niosuser, 'password': niospw}
conn = connector.Connector(opts)

wapiurl = niosutils.get_wapiurl(niosip, niosuser, niospw)

netlist = niosutils.get_nextnets(addr, cidr, wapiurl, niosuser, niospw)
print netlist[0]

addr = netlist[0]

output = gcloudutils.get_network_url(compute, project, parent)
url = output['selfLink']
output = gcloudutils.create_subnet(compute, project, region, url, name, addr)
print output
