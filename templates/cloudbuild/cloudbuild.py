# Copyright 2018 Google Inc. All rights reserved.

""" This template creates a Cloud Build resource. """


def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    outputs = []
    properties = context.properties
    project_id = properties.get('project', context.env['project'])
    name = context.env['name']
    build_steps = properties['steps']
    cloud_build = {
        'name': name,
        # https://cloud.google.com/cloud-build/docs/api/reference/rest/v1/projects.builds/create
        'type': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
        'properties': {
            'projectId': project_id,
            'steps': build_steps
        }
    }

    optional_properties = [
        'source',
        'timeout',
        'images',
        'artifacts',
        'logsBucket',
        'options',
        'substitutions',
        'tags',
        'secrets'
    ]

    for prop in optional_properties:
        if prop in properties:
            cloud_build['properties'][prop] = properties[prop]

    resources.append(cloud_build)

    # Output variables
    output_props = [
        'id',
        'status',
        'results',
        'createTime',
        'startTime',
        'finishTime',
        'logUrl',
        'sourceProvenance'
    ]

    for outprop in output_props:
        output_obj = {}
        output_obj['name'] = outprop
        output_obj['value'] = '$(ref.{}.{})'.format(name, outprop)
        outputs.append(output_obj)

    return {'resources': resources, 'outputs': outputs}
