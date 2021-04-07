# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates External IP address. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    name = context.properties.get('name', context.env['name'])

    resources = [
        {
            'name': context.env['name'],
            'type': 'compute.v1.globalAddress',
            'properties':
                {
                    'name':
                        name,
                    'ipVersion':
                        'IPV4',
                    'networkTier':
                        'PREMIUM'
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
                    'name': 'staticIpName',
                    'value': 'static-ip'
                }
            ]
    }
