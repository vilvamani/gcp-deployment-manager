# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates a Cloud Router. """

def get_network(properties):
    """ Gets a network name. """

    network_name = properties.get('network')
    if network_name:
        is_self_link = '/' in network_name or '.' in network_name

        if is_self_link:
            network_url = network_name
        else:
            network_url = 'global/networks/{}'.format(network_name)

    return network_url

def generate_config(context):
    """ Entry point for the deployment resources. """

    name = context.properties.get('name', context.env['name'])
    project_id = context.properties.get('project', context.env['project'])

    resources = [
        {
            'name': context.env['name'],
            'type': 'compute.v1.router',
            'properties':
                {
                    'name':
                        name,
                    'network':
                        get_network(context.properties),
                    'project':
                        project_id,
                    'region':
                        context.properties['region'],
                    'nats': [{
                        "name": context.properties['nat-name'],
                        "natIpAllocateOption": "AUTO_ONLY",
                        "sourceSubnetworkIpRangesToNat": "LIST_OF_SUBNETWORKS",
                        "subnetworks": [{
                            "name": context.properties['subnet'],
                            "sourceIpRangesToNat": ["PRIMARY_IP_RANGE"]
                        }]
                    }]
                }
        }
    ]

    return {
        'resources':
            resources,
        'outputs':
            [
                {
                    'name': 'name',
                    'value': name
                },
                {
                    'name': 'selfLink',
                    'value': '$(ref.' + context.env['name'] + '.selfLink)'
                },
                {
                    'name':
                        'creationTimestamp',
                    'value':
                        '$(ref.' + context.env['name'] + '.creationTimestamp)'
                }
            ]
    }
