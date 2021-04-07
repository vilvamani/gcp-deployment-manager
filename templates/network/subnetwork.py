# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates a subnetwork. """


def generate_config(context):
    """ Entry point for the deployment resources. """

    props = context.properties
    props['name'] = props.get('name', context.env['name'])
    required_properties = ['name', 'network', 'ipCidrRange', 'region']
    optional_properties = [
        'project',
        'enableFlowLogs',
        'privateIpGoogleAccess',
        'secondaryIpRanges'
    ]

    # Load the mandatory properties, then the optional ones (if specified).
    properties = {p: props[p] for p in required_properties}
    properties.update(
        {
            p: props[p]
            for p in optional_properties
            if p in props
        }
    )

    resources = [
        {
            # https://cloud.google.com/compute/docs/reference/rest/v1/subnetworks/insert
            'type': 'gcp-types/compute-v1:subnetworks',
            'name': context.env['name'],
            'properties': properties
        }
    ]

    output = [
        {
            'name': 'name',
            'value': properties['name']
        },
        {
            'name': 'selfLink',
            'value': '$(ref.{}.selfLink)'.format(context.env['name'])
        },
        {
            'name': 'ipCidrRange',
            'value': '$(ref.{}.ipCidrRange)'.format(context.env['name'])
        },
        {
            'name': 'region',
            'value': '$(ref.{}.region)'.format(context.env['name'])
        },
        {
            'name': 'network',
            'value': '$(ref.{}.network)'.format(context.env['name'])
        },
        {
            'name': 'gatewayAddress',
            'value': '$(ref.{}.gatewayAddress)'.format(context.env['name'])
        }
    ]

    return {'resources': resources, 'outputs': output}
