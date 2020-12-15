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
          'steps': [
              {
                  'id': 'git_clone',
                  'name': 'gcr.io/cloud-builders/git',
                  'args': ['clone', '-b', 'develop', 'https://github.com/vilvamani/gcp-deployment-manager.git', 'quick_start']
              }
          ],
          'timeout': '120s'
      }
  }]
  
  return { 'resources': resources }
