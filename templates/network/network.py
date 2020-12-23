# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates a network, optionally with subnetworks. """


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
    network_self_link = '$(ref.{}.selfLink)'.format(context.env['name'])

    network_resource = {
        # https://cloud.google.com/compute/docs/reference/rest/v1/networks/insert
        'type': 'gcp-types/compute-v1:networks',
        'name': context.env['name'],
        'properties':
            {
                'name': name,
                'autoCreateSubnetworks': properties.get('autoCreateSubnetworks', False)
        }
    }
    optional_properties = [
        'description',
        'routingConfig',
        'project',
    ]
    for prop in optional_properties:
        append_optional_property(network_resource, properties, prop)
    resources = [network_resource]

    # Subnetworks:
    out = {}
    for i, subnetwork in enumerate(
        properties.get('subnetworks', []), 1
    ):
        subnetwork['network'] = network_self_link
        if properties.get('project'):
            subnetwork['project'] = properties.get('project')

        subnetwork_name = 'subnetwork-{}'.format(i)
        resources.append(
            {
                'name': subnetwork_name,
                'type': 'subnetwork.py',
                'properties': subnetwork
            }
        )

        out[subnetwork_name] = {
            'selfLink': '$(ref.{}.selfLink)'.format(subnetwork_name),
            'ipCidrRange': '$(ref.{}.ipCidrRange)'.format(subnetwork_name),
            'region': '$(ref.{}.region)'.format(subnetwork_name),
            'network': '$(ref.{}.network)'.format(subnetwork_name),
            'gatewayAddress': '$(ref.{}.gatewayAddress)'.format(subnetwork_name)
        }

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
                    'value': network_self_link
                },
                {
                    'name': 'subnetworks',
                    'value': out
                }
            ]
    }
