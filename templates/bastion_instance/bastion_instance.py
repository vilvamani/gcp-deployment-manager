# Copyright 2017 Google Inc. All rights reserved.

"""Creates an autoscaled managed instance group."""
# This consists of multiple resources:
# - Instance Template to define the properties for each VM
#      The image and machine size are hardcoded. They could be parameterized
# - Instance Group Manager
# - Autoscaler to grow and shrink the size of the the Instance Group
# - Load Balancer to distribute traffice to the VMs.


URL_BASE = 'https://www.googleapis.com/compute/v1/projects/'

# Every Python Template needs to have the GenerateConfig() or generate_config()
# method
# This method is called by DM in expansion and must return either:
#    - the yaml format required by DM
#    - a python dictionary representing the yaml (this is more efficient)


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
                  'machineType':
                      context.properties['machineType'],
                  'networkInterfaces': [{
                      'network':
                          context.properties['network'],
                      'subnetwork':
                          context.properties['publicsubnet'],
                      'accessConfigs': [{
                          'name': 'External NAT',
                          'type': 'ONE_TO_ONE_NAT'
                      }]
                  }],
                  'metadata': {
                      'items': [{
                          'key': 'startup-script',
                          'value': |
                            #!/bin/bash
                            #### Log the execution to a file ####
                            exec 3>&1 4>&2
                            trap 'exec 2>&4 1>&3' 0 1 2 3 RETURN
                            exec 1>/var/log/configure-bastion.log 2>&1

                            set -x
                            #install kubectl
                            curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl"
                            chmod +x ./kubectl
                            sudo mv ./kubectl /usr/local/bin/kubectl
                            kubectl version --client

                            #mount filestore
                            sudo yum -y update && sudo yum -y install nfs-utils
                            sudo mkdir -p /mnt/boominfs
                            sudo mount  context.properties["fileShareIp"]:/boomifileshare /mnt/boominfs

                            export HOME='whoami'
                            export KUBECONFIG=$HOME/.kube/config
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
