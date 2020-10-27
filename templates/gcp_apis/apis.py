# Copyright 2018 Google Inc. All rights reserved.

""" This template enable GCP APIs. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    for api in context.properties['apis']:

        resources.append(
            {
                'name': api['name'],
                'action': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
                'properties': 
                    {
                        'consumerId': context.properties['consumerId'],
                        'serviceName': api['serviceName']
                    }
            }
        )


    return {
        'resources':
            resources,
        'outputs':
            [
                {
                    'name': 'vpcName',
                    'value': api['name']
                }
            ]
    }