# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates a Cloud Router. """


def append_optional_property(res, properties, prop_name):
    """ If the property is set, it is added to the resource. """

    val = properties.get(prop_name)
    if val:
        res['properties'][prop_name] = val
    return


def generate_config(context):
    """ Entry point for the deployment resources. """

    properties = context.properties
    name = properties.get('name', context.env['name'])
    project_id = properties.get('project', context.env['project'])

    bgp = properties.get('bgp', {'asn': properties.get('asn')})

    router = {
        'name': context.env['name'],
        # https://cloud.google.com/compute/docs/reference/rest/v1/routers
        'type': 'gcp-types/compute-v1:routers',
        'properties':
            {
                'name':
                    name,
                'project':
                    project_id,
                'region':
                    properties['region'],
                'network':
                    properties.get('networkURL', generate_network_uri(
                        project_id,
                        properties.get('network', ''))),
        }
    }

    if properties.get('bgp'):
        router['properties']['bgp'] = bgp

    optional_properties = [
        'description',
        'bgpPeers',
        'interfaces',
        'nats',
    ]

    for prop in optional_properties:
        append_optional_property(router, properties, prop)

    return {
        'resources': [router],
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


def generate_network_uri(project_id, network):
    """Format the network name as a network URI."""

    return 'projects/{}/global/networks/{}'.format(
        project_id,
        network
    )
