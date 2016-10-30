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
	epilog='Example: \'./create_vm.py 10.138.0.0 test test.com --count 2\' will create two VMs, test1.test.com and test2.test.com')
parser.add_argument('subnet', nargs=1, help='Subnet in which to create the VMs')
parser.add_argument('prefix', default='test', help='Prefix for the VM names')
parser.add_argument('dnszone', help='DNS zone where host records will be created')
parser.add_argument('--count', dest='num', type=int, default=1, help='Number of VMs to create')
args=parser.parse_args()
subnet = args.subnet[0]
num = args.num

niosip = '10.60.27.4'
niosuser = 'admin'
niospw = 'infoblox'
project='mythic-brook-146218'
zone='us-west1-a'
nameprefix = args.prefix
dnszone = args.dnszone

opts = {'host': niosip, 'username': niosuser, 'password': niospw}
conn = connector.Connector(opts)

wapiurl = niosutils.get_wapiurl(niosip, niosuser, niospw)

iplist = niosutils.get_nextips(subnet, num, wapiurl, niosuser, niospw)

i = 1
for addr in iplist:
	name = nameprefix + str(i)
	output = gcloudutils.create_instance(compute, project, zone, name, addr)
	operation = (output['name'])
	gcloudutils.wait_for_operation(compute, project, zone, operation)
	host = name + '.' + dnszone
	print 'Creating record %s' % host
	my_ip = objects.IP.create(ip=addr)
	hr = objects.HostRecord.create(conn, name=host, ip=my_ip)
	print hr
	i += 1
