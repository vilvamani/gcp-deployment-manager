# Copyright 2018 Google Inc. All rights reserved.

""" This template enable GCP APIs. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    name = context.properties.get('name') or context.env['name']

    resources = [
        {
            'type': 'compute.v1.globalAddress',
            'name': name,
            'properties': 
            {
                'name': name,
                'ipVersion': 'IPV4'
            }
        }
    ]


    return {
        'resources':
            resources,
        'outputs':
            [
                {
                    'name': 'ingressStaticIpName',
                    'value': name
                }
            ]
    }