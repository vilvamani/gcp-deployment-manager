# Copyright 2020 Dell Boomi. All rights reserved.

""" This template creates a Google Kubernetes Engine cluster. """
import time

def generate_config(context):
    """ Entry point for the deployment resources. """

    resources = []
    outputs = []
    project_id = context.env['project']
    properties = context.properties
    cluster_type = properties.get('clusterLocationType')
    propc = properties['cluster']
    name = propc.get('name', context.env['name'])
    gke_cluster = {
        'name': name,
        'type': '',
        'properties':
            {
                'cluster':
                    {
                        'name':
                            name,
                        'initialClusterVersion':
                            propc.get('initialClusterVersion')
                    }
            }
    }

    starttime = f'{time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}'
    nextyear = int(time.strftime("%Y", time.gmtime())) + 1
    endtime = f'{nextyear}-{time.strftime("%m-%dT%H:%M:%SZ", time.gmtime())}'

    maintenancePolicy = {
        'window': {
            'recurringWindow': {
                'window': {
                    'startTime': starttime,
                    'endTime': endtime
                },
                'recurrence': "FREQ=MONTHLY;BYSETPOS=1;BYDAY=SA,SU"
            }
        }
    }

    if cluster_type == 'Regional':
        provider = 'gcp-types/container-v1beta1:projects.locations.clusters'
        if not properties.get('region'):
            raise KeyError(
                "region is a required property for a {} Cluster.".
                format(cluster_type)
            )
        parent = 'projects/{}/locations/{}'.format(
            project_id,
            properties.get('region')
        )
        gke_cluster['properties']['parent'] = parent

    elif cluster_type == 'Zonal':
        provider = 'container.v1.cluster'
        if not properties.get('zone'):
            raise KeyError(
                "zone is a required property for a {} Cluster.".
                format(cluster_type)
            )
        gke_cluster['properties']['zone'] = properties.get('zone')

    gke_cluster['type'] = provider

    cluster_props = gke_cluster['properties']['cluster']

    req_props = ['network', 'subnetwork']

    for prop in req_props:
        cluster_props[prop] = propc.get(prop)
        if prop not in propc:
            raise KeyError(
                "{} is a required cluster property for a {} Cluster.".format(
                    prop,
                    cluster_type
                )
            )

    # optional properties
    optional_props = [
        'description',
        'nodePools',
        'masterAuth',
        'loggingService',
        'monitoringService',
        'clusterIpv4Cidr',
        'addonsConfig',
        'locations',
        'enableKubernetesAlpha',
        'resourceLabels',
        'labelFingerprint',
        'legacyAbac',
        'networkPolicy',
        'ipAllocationPolicy',
        'masterAuthorizedNetworksConfig',
        'maintenancePolicy',
        'binaryAuthorization',
        'podSecurityPolicyConfig',
        'autoscaling',
        'privateClusterConfig',
        'verticalPodAutoScaling',
        'defaultMaxPodsConstraint'
    ]

    for oprop in optional_props:
        if oprop == 'maintenancePolicy':
            cluster_props[oprop] = maintenancePolicy
        if oprop in propc:
            cluster_props[oprop] = propc[oprop]

    resources.append(gke_cluster)

    # Output variables
    output_props = [
        'name',
        'selfLink',
        'endpoint',
        'currentMasterVersion',
        'servicesIpv4Cidr',
        'instanceGroupUrls'
    ]

    for outprop in output_props:
        output_obj = {}
        output_obj['name'] = outprop
        if outprop == 'instanceGroupUrls':
            for index, _ in enumerate(propc['nodePools']):
                output_obj['value'] = '$(ref.{}.nodePools[{}].{})'.format(
                    name,
                    str(index),
                    outprop
                )
        else:
            output_obj['value'] = '$(ref.{}.{})'.format(name, outprop)

        outputs.append(output_obj)

    return {'resources': resources, 'outputs': outputs}