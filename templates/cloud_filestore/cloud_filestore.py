# Copyright 2018 Google Inc. All rights reserved.

""" This template creates a Google Cloud Filestore instance. """


def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    properties = context.properties
    project_id = properties.get('project', context.env['project'])
    name = properties.get('name', context.env['name'])

    resource = {
        'name': context.env['name'],
        # https://cloud.google.com/filestore/docs/reference/rest/v1beta1/projects.locations.instances/create
        'type': 'gcp-types/file-v1beta1:projects.locations.instances',
        'properties': {
            'parent': 'projects/{}/locations/{}'.format(project_id, properties['location']),
            'instanceId': name,
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
                }
            ]
    }