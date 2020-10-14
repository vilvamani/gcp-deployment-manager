# gcp-deployment-manager

```
git clone https://github.com/vilvamani/gcp-deployment-manager.git && cd gcp-deployment-manager
```

```
gcloud deployment-manager deployments create boomi-quickstart --config=test_config.yaml
```

# GKE Credentials
```
gcloud container clusters get-credentials  boomi-quickstart-gke-cluster --zone=us-central1
```