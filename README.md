# pubsub-twitter-stream-python

This repository contains the `twitter-to-pubsub` app that shows how to stream Tweets to a [Google Cloud PubSub](https://cloud.google.com/pubsub/docs) topic. This app is an alternative/updated version of the GoogleCloudPlatform `pubsub` app in [kubernetes-bigquery-python](https://github.com/GoogleCloudPlatform/kubernetes-bigquery-python/tree/master/pubsub). This new version attempts to improve on the original in the following ways:

**Python Client Library**

This new version uses the [Google Python Client Library](https://cloud.google.com/compute/docs/tutorials/python-guide) instead of the standard HTTP client. In general, using client libraries provides better language integration, improved security, and support for making calls that require user authorization. For example, in this context it means we can use a service account and that possible Pub/Sub batch settings can be handled by the client library.

**Tweepy: on_status trigger**

The new code only publishes data to Pub/Sub when tweepy's [on\_status](https://github.com/tweepy/tweepy/blob/78d2883a922fa5232e8cdfab0c272c24b8ce37c4/tweepy/streaming.py#L86) is triggered by a new status. In the original version,  [on\_data](https://github.com/tweepy/tweepy/blob/78d2883a922fa5232e8cdfab0c272c24b8ce37c4/tweepy/streaming.py#L43) is used which also includes streaming Twitter data on deletes, events, direct messages, friends, limits, disconnects and warnings.

**Google Kubernetes Engine** 

The new example includes updated documentation for running the app in [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/docs/).

**Authenticating to Cloud Pub/Sub using a service account**

This app implements an example of authenticating to Cloud Pub/Sub using a service account and subscribes to messages published to a Pub/Sub topic from a Python-based application.

**Dataflow pipeline for streaming Pub/Sub to BigQuery**

See [dataflow-twitter-stream-java](https://github.com/svanstiphout/dataflow-twitter-stream-java)