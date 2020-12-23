# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates firewall rules for a network. """

from hashlib import sha1


def generate_config(context):
    """ Entry point for the deployment resources. """

    properties = context.properties
    project_id = properties.get('project', context.env['project'])
    network = properties.get('network')
    if network:
        if not ('/' in network or '.' in network):
            network = 'global/networks/{}'.format(network)
    else:
        network = 'projects/{}/global/networks/{}'.format(
            project_id,
            properties.get('networkName', 'default')
        )

    resources = []
    out = {}
    for i, rule in enumerate(properties['rules'], 1000):
        res_name = sha1(rule['name'].encode('utf-8')).hexdigest()[:10]

        rule['network'] = network
        rule['priority'] = rule.get('priority', i)
        rule['project'] = project_id
        resources.append(
            {
                'name': res_name,
                'type': 'gcp-types/compute-v1:firewalls',
                'properties': rule
            }
        )

        out[res_name] = {
            'selfLink': '$(ref.' + res_name + '.selfLink)',
            'creationTimestamp': '$(ref.' + res_name
                                 + '.creationTimestamp)',
        }

    outputs = [{'name': 'rules', 'value': out}]

    return {'resources': resources, 'outputs': outputs}
