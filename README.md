# quickstart-boomi-gke-molecule

### Step 1: Adding IAM SecurityAdmin Role to [project-no]@cloudservices.gserviceaccount.com

```
gcloud projects add-iam-policy-binding [project-id] --member=serviceAccount:[project-no]@cloudservices.gserviceaccount.com --role=roles/iam.securityAdmin
```

### Step 2: Open GCP CloudShell and clone the project repository.

```
git clone -b develop https://github.com/vilvamani/gcp-deployment-manager.git  boomi_quickstart && cd boomi_quickstart
```

### Step 3: Update Boomi Username, Password and Account details in the config.jinja file or config.jinja.schema.

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

### Step 4: Execute below command on CloudShell

```
gcloud deployment-manager deployments create boomi --config=config.yaml
```
