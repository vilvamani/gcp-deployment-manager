# Copyright 2018 Google Inc. All rights reserved.

""" This template creates a Google Cloud Filestore instance. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    properties = context.properties
    project_id = properties.get('project', context.env['project'])
    name = properties.get('name', context.env['name'])

    apiresource = {
        'name': 'enableapi',
        'action': 'gcp-types/servicemanagement-v1:servicemanagement.services.enable',
        'properties': {
            'consumerId': 'project:{}'.format(context.env['project']),
            'serviceName': 'file.googleapis.com'
        }
    }

    resources.append(apiresource)

    resource = {
        'name': context.env['name'],
        # https://cloud.google.com/filestore/docs/reference/rest/v1beta1/projects.locations.instances/create
        'type': 'gcp-types/file-v1beta1:projects.locations.instances',
        'properties': {
            'parent': 'projects/{}/locations/{}'.format(project_id, properties['location']),
            'instanceId': name,
        },
        'metadata': {
            'dependsOn': ['enableapi']
        }
    }

    optional_props = [
        'description',
        'tier',
        'labels',
        'fileShares',
        'networks',
    ]

    for prop in optional_props:
        if prop in properties:
            resource['properties'][prop] = properties[prop]

    resources.append(resource)

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
                    'name': 'fileShares',
                    'value': '$(ref.{}.fileShares)'.format(context.env['name'])
                },
                {
                    'name': 'networks',
                    'value': '$(ref.{}.networks)'.format(context.env['name'])
                },
                {
                    'name': 'fileShareIp',
                    'value': '$(ref.{}.networks[0].ipAddresses[0])'.format(context.env['name'])
                }
            ]
    }
