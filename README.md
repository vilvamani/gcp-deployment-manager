# quickstart-boomi-gke-molecule

## Setting up

1. Select or create a Google Cloud Platform project:

    <walkthrough-project-setup></walkthrough-project-setup>

1. [Enable billing](https://support.google.com/cloud/answer/6293499#enable-billing).

1. Configure the `gcloud` command-line tool to use your project:

    ```sh
	  gcloud config set project {{project-id}}
    ```

1. Run this command to enable the Deployment Manager and Compute APIs:

    ```sh
    gcloud services enable compute.googleapis.com deploymentmanager.googleapis.com  
    ```

## Adding IAM SecurityAdmin Role to [project-no]@cloudservices.gserviceaccount.com

```
gcloud projects add-iam-policy-binding [project-id] --member=serviceAccount:[project-no]@cloudservices.gserviceaccount.com --role=roles/iam.securityAdmin
```

## Open GCP CloudShell and clone the project repository.

To begin, run these commands to open the quickstart

```sh
git clone -b develop https://github.com/vilvamani/gcp-deployment-manager.git  boomi_quickstart && cd boomi_quickstart
```

## Securely store sensitive data in secret manager.

```
  echo -n "vilvamani007@gmail.com" | gcloud secrets create boomiUserEmailID --replication-policy="automatic" --data-file=-

  echo -n "google#2020" | gcloud secrets create boomiPassword --replication-policy="automatic" --data-file=-
  
  echo -n "google-microsoft" | gcloud secrets create boomiAccountID --replication-policy="automatic" --data-file=-

```
## Update Boomi Username, Password and Account details in the config.jinja file or config.jinja.schema.

```
  secretEmailID:
    type: string
    default: boomiUserEmailID

  secretPassword:
    type: string
    default: boomiPassword

  secretAccountID:
    type: string
    default: boomiAccountID
```

## Deploy the resources

To deploy your resources, use the `gcloud` command-line tool to create a new
deployment, using your configuration file:

```sh
gcloud deployment-manager deployments create boomi-quickstart --config=test_data/config.yaml
```

To deploy your resources in the existing network, use the `gcloud` command-line tool to create a new
deployment, using your configuration file:

```sh
gcloud deployment-manager deployments create boomi-quickstart --config=test_data/config_existing_vpc.yaml
```

## Check on your deployment

To check the status of the deployment, run this command:

```sh
gcloud deployment-manager deployments describe boomi-quickstart
```

## Review your resources

After you have created the deployment, you can review your resources in the
Cloud console.

1. To see a list of your deployments,
    [open the Deployment Manager page](https://console.cloud.google.com/dm/deployments).

1. To see the resources in the deployment, click **quickstart-deployment**. The
   deployment overview opens, with information about the deployment, and the
   resources that are part of the deployment.

## Clean up

To avoid incurring charges on your Cloud Platform account, delete the deployment and
all the resources that you created:

```sh
gcloud deployment-manager deployments delete boomi-quickstart
```

## Deploying or updating applications in the existing private kuberenetes cluster

- The private GKE cluster has Public endpoint access enabled and authorized networks enabled. Machines with public IP addresses can use kubectl to communicate with the public endpoint only if their public IP addresses are included in the list of authorized networks.
- To update the GKE cluster via deployment manager make sure the disable the master authorised network using below command before updating the deployment:
```
  gcloud container clusters update CLUSTER_NAME --no-enable-master-authorized-networks --region region 
```
Reference document : https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept#overview

## Security best practices

When creating new project set organizational level policy constraint to skip default network creation.
Reference document : https://cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints#constraints-for-specific-services
