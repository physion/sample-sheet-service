#!/usr/bin/env bash

#!/bin/bash

RELEASE_PREFIX=$1
NAMESPACE=$(echo $2 | tr '[:upper:]' '[:lower:]')
IMAGE_TAG=$3

echo "./deploy.sh $RELEASE_PREFIX $NAMESPACE $IMAGE_TAG"

if [ -z "$IMAGE_TAG" ]; then
  IMAGE_TAG=$NAMESPACE
fi

set -e

RELEASE_NAME=$RELEASE_PREFIX-$NAMESPACE
GCP_REGION=us-east1
KUBERNETES_CLUSTER_NAME=ovation2

codeship_google authenticate
export GOOGLE_APPLICATION_CREDENTIALS=/keyconfig.json

gcloud container clusters get-credentials $KUBERNETES_CLUSTER_NAME \
  --project $GOOGLE_PROJECT_ID \
  --zone $GCP_REGION


echo "Setting Project ID $PROJECT_ID"
gcloud config set project $GOOGLE_PROJECT_ID

echo "Setting default timezone $GCP_REGION"
gcloud config set compute/zone $GCP_REGION

# Install helm
curl https://raw.githubusercontent.com/kubernetes/helm/master/scripts/get | bash
helm init --upgrade --force-upgrade

# Install helm-secrets
echo "Installing helm-secrets"
helm plugin install https://github.com/futuresimple/helm-secrets

echo "Upgrading release..."

echo "NAMESPACE = $NAMESPACE"
echo "RELEASE_NAME = $RELEASE_NAME"
echo "CI_TIMESTAMP = $CI_TIMESTAMP"

echo "helm secrets upgrade --install --namespace=${NAMESPACE} --timeout 600 --wait \
    --set image.tag=${IMAGE_TAG}-${CI_TIMESTAMP} \
    -f ./deploy/values/${NAMESPACE}/secrets.yaml \
    ${RELEASE_NAME} \
    ./deploy/ovation-io/"

helm secrets upgrade --install --namespace=${NAMESPACE} --timeout 600 --wait \
    --set image.tag=${IMAGE_TAG}-${CI_TIMESTAMP} \
    -f ./deploy/values/${NAMESPACE}/secrets.yaml \
    ${RELEASE_NAME} \
    ./deploy/ovation-io/
