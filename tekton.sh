
#!/bin/zsh


# Install the latest version of Tekton Pipelines
kubectl apply -f https://storage.googleapis.com/tekton-releases/pipeline/latest/release.yaml

# Check that the Tekton controllers are running
kubectl get pods -n tekton-pipelines




brew tap tektoncd/tools
brew install tektoncd/tools/tektoncd-cli

# Tekton Dashboard
kubectl apply --filename https://storage.googleapis.com/tekton-releases/dashboard/latest/release-full.yaml


# Tekton Triggers

kubectl apply --filename \
https://storage.googleapis.com/tekton-releases/triggers/latest/release.yaml
kubectl apply --filename \
https://storage.googleapis.com/tekton-releases/triggers/latest/interceptors.yaml

