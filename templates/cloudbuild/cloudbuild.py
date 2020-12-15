"""Creates a Cloud Container Builder build."""

import json


def GenerateConfig(context):
  """Generate YAML resource configuration."""
  
  name = context.env['name'] + '-cloudbuild'

  resources = [{
      'name': name,
      'action': 'gcp-types/cloudbuild-v1:cloudbuild.projects.builds.create',
      'metadata': {
          'runtimePolicy': ['UPDATE_ALWAYS']
      },
      'properties': {
          'timeout': '120s',
          'substitutions': {
              '_HELM_VERSION': '3.2.0'
          },
          'steps': [
              {
                  'id': 'git_clone',
                  'name': 'gcr.io/cloud-builders/git',
                  'args': ['clone', '-b', 'develop', 'https://github.com/vilvamani/gcp-deployment-manager.git', 'quick_start']
              },
              {
                  'id': 'build_image',
                  'name': 'gcr.io/cloud-builders/docker',
                  'args': ['build', '--tag=gcr.io/$PROJECT_ID/helm:${_HELM_VERSION}', '--tag=gcr.io/$PROJECT_ID/helm:latest', '--build-arg', 'HELM_VERSION=v${_HELM_VERSION}', '.'],
                  'dir': 'quick_start/kubernetes',
                  'waitFor': ['git_clone']
              }
          ]
      }
  }]
  
  return { 'resources': resources }
