#!/usr/bin/python

import niosutils
import gcloudutils
import sys
import requests
import json
import re
from infoblox_client import connector
from infoblox_client import objects
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
credentials = GoogleCredentials.get_application_default()
compute = discovery.build('compute', 'v1', credentials=credentials)

subnet = sys.argv[1]
num = sys.argv[2]

niosip = '10.60.27.4'
niosuser = 'admin'
niospw = 'infoblox'
project='mythic-brook-146218'
zone='us-west1-a'
nameprefix='test'
dnszone='test.com'

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
