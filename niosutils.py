import sys
import requests
import json
import re
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning

def get_wapiurl(niosip, niosuser, niospw):
	# Determine the WAPI version and get the WAPI URL
	docurl = 'https://%s/wapidoc/' % niosip
	r = requests.get(docurl, verify=False)
	version = re.search(r'^\s*VERSION:\s*\'(.*)\',', r.text, re.MULTILINE)
	wapiversion = version.group(1)
	wapiurl = 'https://%s/wapi/v%s/' % (niosip, wapiversion)
	return wapiurl

def get_nextips(subnet, num, wapiurl, niosuser, niospw):
	# Get the network object reference
	joburl = wapiurl + 'network'
	payload = {'network': subnet}
	resp = requests.get(joburl, auth=HTTPBasicAuth(niosuser, niospw),verify=False,params=payload)
	j = resp.json()
	k = j[0]
	netref = k['_ref']
	# Get the requested number of IPs and return a list
	joburl = wapiurl + netref + '?_function=next_available_ip'
	payload = {'num': num}
	resp = requests.post(joburl, auth=HTTPBasicAuth(niosuser, niospw),verify=False,params=payload)
	j = resp.json()
	k = j['ips']
	return k

#def create_host(host, ip, wapiurl, niosuser, niospw):
#	joburl = wapiurl + 'record:host'
#	print joburl
#	payload = '{"ipv4addrs": [{"ipv4addr": "10.138.0.2"}], "name": "test1.test.com"}'
#	print payload
#	resp = requests.post(joburl, auth=HTTPBasicAuth(niosuser, niospw),verify=False,params=payload)
#        j = resp.json()
#	return j
