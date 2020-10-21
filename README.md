# gcp-deployment-manager

```
gcloud projects add-iam-policy-binding [project-id] --member=serviceAccount:[project-no]@cloudservices.gserviceaccount.com --role=roles/resourcemanager.projectIamAdmin
```

```
gcloud projects add-iam-policy-binding [project-id] --member=serviceAccount:[project-no]@cloudservices.gserviceaccount.com --role=roles/iam.securityAdmin
```

```
git clone https://github.com/vilvamani/gcp-deployment-manager.git && cd gcp-deployment-manager
```

```
gcloud deployment-manager deployments create boomi-qs --config=test_config.yaml
```

# GKE Credentials
```
gcloud container clusters get-credentials  boomi-qs-gke-cluster --zone=us-central1
```