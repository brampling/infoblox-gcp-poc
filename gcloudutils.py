import sys
from time import sleep
from oauth2client.client import GoogleCredentials
from googleapiclient import discovery

def create_instance(compute, project, zone, name, addr):
    image_response = compute.images().getFromFamily(
        project='debian-cloud', family='debian-8').execute()
    source_disk_image = image_response['selfLink']
    machine_type = "zones/%s/machineTypes/f1-micro" % zone

    config = {
        'name': name,
        'machineType': machine_type,
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        'networkInterfaces': [{
            'network': 'global/networks/default',
            'networkIP': addr,
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
            }]
        }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

def create_network(compute, project, name):
	config = {'name': name, 'autoCreateSubnetworks': False}
	return compute.networks().insert(
		project=project,
		body=config).execute()

def get_network_url(compute, project, name):
	return compute.networks().get(
		project=project,
		network=name).execute()
	
def create_subnet(compute, project, zone, parent, name, addr):
	config = {'name': name, 'network': parent, 'ipCidrRange': addr}
	return compute.subnetworks().insert(
		project=project,
		region=zone,
		body=config).execute()

def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        sleep(5)

def delete_instance(compute, project, zone, name):
        return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
