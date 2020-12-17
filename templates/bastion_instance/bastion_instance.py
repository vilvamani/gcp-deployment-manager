# Copyright 2020 Dell Boomi. All rights reserved.

"""Creates an autoscaled managed instance group."""

URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

def GenerateConfig(context):
  """Generates the configuration."""

  deployment = context.env['deployment']
  instance_template = deployment + '-it'
  igm = deployment + '-igm'
  region = context.properties['region']

  # Create a dictionary which represents the resources
  # (Intstance Template, IGM, etc.)
  resources = [
      {
          # Create the Instance Template
          'name': instance_template,
          'type': 'compute.v1.instanceTemplate',
          'properties': {
              'properties': {
                  'serviceAccounts': [{
                      'email': 
                          context.properties['serviceAccountEmail'],
                       'scopes':
                          context.properties['serviceAccountScopes']
                  }],
                  'tags': context.properties['tags'],
                  'machineType':
                      context.properties['machineType'],
                  'networkInterfaces': [{
                      'network':
                          context.properties['network'],
                      'subnetwork':
                          context.properties['subnetworks'],
                      'accessConfigs': [{
                          'name': 'External NAT',
                          'type': 'ONE_TO_ONE_NAT'
                      }]
                  }],
                  'metadata': {
                      'items': [{
                          'key': 'startup-script',
                          'value': context.properties['startupScript']
                        }]
                  },
                  'disks': [{
                      'deviceName': 'boot',
                      'type': 'PERSISTENT',
                      'boot': True,
                      'autoDelete': True,
                      'diskType': 'pd-ssd',
                      'diskSizeGb': '30',
                      'mode': 'READ_WRITE',
                      'initializeParams': {
                          'sourceImage':
                              URL_BASE +
                              context.properties['machineImage']
                      }
                  }]
              }
          }
      },
      {
          # Instance Group Manager
          'name': igm,
          'type': 'compute.v1.regionInstanceGroupManager',
          'properties': {
              'region': region,
              'failoverAction': 'NO_FAILOVER',
              'baseInstanceName': deployment + '-instance',
              'instanceTemplate': '$(ref.' + instance_template + '.selfLink)',
              'targetSize': 1
          }
      },
      {
          # Autoscaler
          'name': deployment + '-as',
          'type': 'compute.v1.regionAutoscaler',
          'properties': {
              'target': '$(ref.' + igm + '.selfLink)',
              'region': region,
              'autoscalingPolicy': {
                  'minNumReplicas': context.properties['minSize'],
                  'maxNumReplicas': int(context.properties['maxSize']),
                  'cpuUtilization': {
                      'utilizationTarget': 0.8
                  },
                  'coolDownPeriodSec': 90
              }
          }
      }
  ]

  return {'resources': resources}
