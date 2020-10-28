# Copyright 2018 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
""" This template creates a Cloud Router. """
def get_network(properties):
    """ Gets a network name. """

    network_name = properties.get('network')
    if network_name:
        is_self_link = '/' in network_name or '.' in network_name

        if is_self_link:
            network_url = network_name
        else:
            network_url = 'global/networks/{}'.format(network_name)

    return network_url

def generate_config(context):
    """ Entry point for the deployment resources. """

    name = context.properties.get('name', context.env['name'])

    resources = [
        {
            'name': context.env['name'],
            'type': 'compute.v1.router',
            'properties':
                {
                    'name':
                        name,
                    'bgp': {
                        'asn': context.properties['asn']
                    },
                    'network':
                        get_network(context.properties),
                    'region':
                        context.properties['region']
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
                    'name': 'selfLink',
                    'value': '$(ref.' + context.env['name'] + '.selfLink)'
                },
                {
                    'name':
                        'creationTimestamp',
                    'value':
                        '$(ref.' + context.env['name'] + '.creationTimestamp)'
                }
            ]
    }