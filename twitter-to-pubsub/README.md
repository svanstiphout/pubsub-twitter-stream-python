# twitter-to-pubsub

(TODO) Document steps to: 

* Install the Google Cloud SDK
* Enable the Google Kubernetes Engine API
* Pub/Sub Topic and Subscribtion setup
* Update twitter-to-pubsub.yaml

# Run App on Google Kubernetes Engine

*Step 0: Update gloud components*

	$ gcloud components update

**Step 1: Build the container image and tag it for uploading**

	$ docker build -t gcr.io/<PROJECT_ID>/<APP>:<TAG> <IMAGE>
	$ docker build -t gcr.io/<PROJECT_ID>/twitter-to-pubsub:latest twitter-to-pubsub-image

**Step 2: Upload the container image to Google Container Registry**

	$ gcloud docker -- push gcr.io/<PROJECT_ID>/<APP>:<TAG>
	$ gcloud docker -- push gcr.io/<PROJECT_ID>/twitter-to-pubsub:latest

**Step 3: Run locally (optional)**

	$ docker run --rm gcr.io/<PROJECT_ID>/twitter-to-pubsub:latest

**Step 4: Create a container cluster**

	$ gcloud container clusters create twitter-cluster --num-nodes=1

Retrieve cluster credentials and configure kubectl command-line tool:

	$ gcloud container clusters get-credentials twitter-cluster

**Step 5: Create a secret for authenicating to Google Cloud Platform** ([docs](https://cloud.google.com/kubernetes-engine/docs/tutorials/authenticating-to-cloud-platform))

	$ kubectl create secret generic pubsub-key --from-file=key.json=<PATH-TO-KEY-FILE>.json

**Step 6: Deploy app as a workload on Google Kubernetes Engine**

	$ kubectl create -f twitter-to-pubsub.yaml

**Step 7: Clean up**

Delete deployment:

	$ kubectl delete deployment twitter-to-pubsub

Remove container cluster:

	$ gcloud container clusters delete twitter-cluster

Remove container image from Google Container Registry:

	$ gcloud container images delete gcr.io/<PROJECT_ID>/twitter-to-pubsub:latest

Remove local Docker image:

	$ docker images
	$ docker rmi <IMAGE_ID_>
