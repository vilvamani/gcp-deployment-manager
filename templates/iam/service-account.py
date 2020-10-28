# Copyright 2018 Google Inc. All rights reserved.

""" This template creates service account for boomi. """

def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    project_id = context.env['project']
    deployment = context.env['deployment']
    name = deployment + '-boomi-sa'
    
    resources.append(
        {
            'name': name,
            'action': 'iam.v1.serviceAccount',
            'properties': 
                {
                    'accountId': name,
                    'projectId': project_id,
                    'displayName': 'Service Account used by boomi-molecule for admin actions'
                }
        }
    )


    return { 
        'resources': resources, 
        'outputs':
                [
                    {
                        'name': 'boomiServiceAccountEmail',
                        'value': f'$(ref.{name}.email)'
                    }
                ]
            }
