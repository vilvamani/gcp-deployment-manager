"""Creates a Cloud Container Builder build."""

import json


def GenerateConfig(context):
  """Generate YAML resource configuration."""
  
  name = context.env['name'] + '-cloudbuild'
  properties = context.properties
  ipaddress = properties.get('ipaddress')

  resources = [{
      'name': name,
      'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
      'metadata': {
          'runtimePolicy': ['UPDATE_ALWAYS']
      },
      'properties': {
          'timeout': '120s',
          'substitutions': {
              '_HELM_VERSION': '3.2.0',
              '_REGION': properties.get('region'),
              '_CLUSTER_NAME': properties.get('CLUSTER_NAME')
          },
          'steps': [
              {
                  'id': 'git_clone',
                  'name': 'gcr.io/cloud-builders/git',
                  'args': [
                    'clone',
                    '-b',
                    'develop',
                    'https://github.com/vilvamani/gcp-deployment-manager.git',
                    'quick_start'
                   ]
              },
              {
                  'id': 'build_image',
                  'name': 'gcr.io/cloud-builders/docker',
                  'args': [
                    'build',
                    '--tag=gcr.io/$PROJECT_ID/helm:${_HELM_VERSION}',
                    '--tag=gcr.io/$PROJECT_ID/helm:latest',
                    '--build-arg',
                    'HELM_VERSION=v${_HELM_VERSION}',
                    '.'
                   ],
                  'dir': 'quick_start/kubernetes',
                  'waitFor': ['git_clone']
              },
              {
                  'id': 'helm_nfs_deployment',
                  'name': 'gcr.io/$PROJECT_ID/helm:latest',
                  'args': [
                    'upgrade',
                    '--install',
                    'nfsprovisioner',
                    '--set',
                    'nfs.server='+ ipaddress,
                    'nfs.path=/boomifileshare,storageClass.defaultClass=true,storageClass.reclaimPolicy=Retain,storageClass.accessModes=ReadWriteMany',
                    '.'
                   ],
                  'dir': 'quick_start/kubernetes/nfs-client-provisioner',
                  'env': [
                    'CLOUDSDK_COMPUTE_REGION=${_REGION}',
                    'CLOUDSDK_CONTAINER_CLUSTER=${_CLUSTER_NAME}', 
                    'KUBECONFIG=/workspace/.kube/config'
                   ],
                  'waitFor': ['build_image']
              }
          ]
      }
  }]
  
  return { 'resources': resources }
