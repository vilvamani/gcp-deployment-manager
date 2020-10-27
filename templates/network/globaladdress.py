# Copyright 2018 Google Inc. All rights reserved.

""" This template enable GCP APIs. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    name = context.properties.get('name') or context.env['name']

    resources = []
    resources.append(
    {
        'name': name,
        'action': 'gcp-types/compute-v1:globalAddresses',
        'properties': 
            {
                'name': name,
                'ipVersion': 'IPV4',
                'networkTier': 'PREMIUM'
            }
        }
    )

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