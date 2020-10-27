# Copyright 2018 Google Inc. All rights reserved.

""" This template enable GCP APIs. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    resources.append(
        {
            'name': 'fileshare-api',
            'action': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
            'properties': 
                {
                    'consumerId': context.properties['consumerId'],
                    'serviceName': 'file.googleapis.com'
                }
        }
    )

    resources.append(
        {
            'name': context.properties['name'],
            'type': 'cloud_filestore.py',
            'properties': cloud_filestore
        }
    )

    return {'resources': resources}
