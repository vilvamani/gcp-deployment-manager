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

## Update Boomi Username, Password and Account details in the config.jinja file or config.jinja.schema.

```
  boomiUserEmailID:
    type: string
    default: vilvamani007@gmail.com

  boomiPassword:
    type: string
    default: google#2020

  boomiAccountID:
    type: string
    default: google-microsoft
```

## Deploy the resources

To deploy your resources, use the `gcloud` command-line tool to create a new
deployment, using your configuration file:

```sh
gcloud deployment-manager deployments create boomi-quickstart --config=test_data/config.yaml

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
