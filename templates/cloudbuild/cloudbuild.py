"""Creates a Cloud Container Builder build."""

import json


def GenerateConfig(context):
  """Generate YAML resource configuration."""
  
  name = context.env['name'] + '-cloudbuild'
  properties = context.properties
  
  resources = [{
      'name': name,
      'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
      'metadata': {
          'runtimePolicy': ['UPDATE_ALWAYS']
      },
      'properties': {
          'timeout': '300s',
          'substitutions': {
              '_HELM_VERSION': '3.2.0',
              '_REGION': properties.get('region'),
              '_CLUSTER_NAME': properties.get('CLUSTER_NAME'),
              '_IP_ADDRESS': properties.get('ipaddress'),
              '_BOOMIUSEREMAILID': properties.get('boomiUserEmailID'),
              '_BOOMIPASSWORD': properties.get('boomiPassword'),
              '_BOOMIACCOUNTID': properties.get('boomiAccountID'),
              '_RESERVEDIPRANGE': properties.get('ipaddress'),
              '_NETWORK': properties.get('network'),
              '_STATICIPADDRESS': properties.get('ingressStaticIpName')
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
                    'nfs.server=${_IP_ADDRESS},nfs.path=/boomifileshare,storageClass.defaultClass=true,storageClass.reclaimPolicy=Retain,storageClass.accessModes=ReadWriteMany',
                    '.'
                   ],
                  'dir': 'quick_start/kubernetes/nfs-client-provisioner',
                  'env': [
                    'CLOUDSDK_COMPUTE_REGION=${_REGION}',
                    'CLOUDSDK_CONTAINER_CLUSTER=${_CLUSTER_NAME}', 
                    'KUBECONFIG=/workspace/.kube/config'
                   ],
                  'waitFor': ['build_image']
              },
              {
                  'id': 'helm_boomi_deployment',
                  'name': 'gcr.io/$PROJECT_ID/helm:latest',
                  'args': [
                    'upgrade',
                    '--install',
                    'boomimolecule',
                    '--namespace',
                    'default',
                    '--set',
                    'secrets.username=${_BOOMIUSEREMAILID},secrets.password=${_BOOMIPASSWORD},secrets.account=${_BOOMIACCOUNTID},volume.server=${_IP_ADDRESS},storage.reservedIpRange=${_RESERVEDIPRANGE},storage.network=${_NETWORK},ingress.staticIpName=${_STATICIPADDRESS}',
                    '.'
                   ],
                  'dir': 'quick_start/kubernetes/boomi-molecule',
                  'env': [
                    'CLOUDSDK_COMPUTE_REGION=${_REGION}',
                    'CLOUDSDK_CONTAINER_CLUSTER=${_CLUSTER_NAME}', 
                    'KUBECONFIG=/workspace/.kube/config'
                   ],
                  'waitFor': ['helm_nfs_deployment']
              },
              {
                  'id': 'kubectl_hpa_deployment',
                  'name': 'gcr.io/cloud-builders/kubectl',
                  'args': [
                    'apply',
                    '--filename=./templates/boomi_molecule_gke_hpa.yaml',
                    '--validate=false'
                   ],
                  'dir': 'quick_start/kubernetes/boomi-molecule',
                  'env': [
                    'CLOUDSDK_COMPUTE_REGION=${_REGION}',
                    'CLOUDSDK_CONTAINER_CLUSTER=${_CLUSTER_NAME}', 
                    'KUBECONFIG=/workspace/.kube/config'
                   ],
                  'waitFor': ['helm_boomi_deployment']
              },
              {
                  'id': 'enable_master_authorized_network',
                  'name': 'gcr.io/cloud-builders/gcloud',
                  'entrypoint': 'bash',
                  'args': [
                    '-c',
                    'gcloud container clusters update ${_CLUSTER_NAME} --enable-master-authorized-networks --region ${_REGION}'
                   ],
                  'waitFor': ['kubectl_hpa_deployment']
              }
          ]
      }
  }]
  
  return { 'resources': resources }
