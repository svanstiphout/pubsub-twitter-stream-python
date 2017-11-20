#!/usr/bin/env python

"""This script uses the Twitter Streaming API to stream tweets 
and publish them to a Google Pub/Sub topic using the 
Google Cloud Python client library. 

This project is an alternative/updated version of 
GoogleCloudPlatform's pubsub app in kubernetes-bigquery-python

https://github.com/GoogleCloudPlatform/kubernetes-bigquery-python
"""

import json
import logging
import os

from google.cloud import pubsub_v1
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

# Environmental vairbales are set in twitter-stream.yaml
# Get Twitter credentials from environment variables
CONSUMER_KEY = os.environ['CONSUMERKEY']
CONSUMER_SECRET = os.environ['CONSUMERSECRET']
ACCESSS_TOKEN = os.environ['ACCESSTOKEN']
ACCESSS_TOKEN_SECRET = os.environ['ACCESSTOKENSEC']

# Get GCP project and topic from environment variables
GCP_PROJECT = os.environ['GCP_PROJECT']
PUBSUB_TOPIC = os.environ['PUBSUB_TOPIC']

# Set number of Tweets to tricker restart and 
MAX_TWEETS = 10000000
LOG_COUNT = 1000


class StdOutListener(StreamListener):
    """A listener handles tweets that are received from the stream.
    This listener dumps the tweets into a PubSub topic
    """

    def __init__(self):
        super().__init__()
        self.count = 0
        self.total_tweets = MAX_TWEETS

        # Instantiates a pubsub client
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(GCP_PROJECT, 
            PUBSUB_TOPIC)

        # Below can be used to configure the batch settings to publish 
        # once there is one kilobyte of data or 1 second has passed.
        
        # batch_settings = pubsub_v1.types.BatchSettings(
        #     max_bytes=1024,  # One kilobyte
        #     max_latency=1,  # One second
        # )
        # self.publisher = pubsub_v1.PublisherClient(batch_settings)

    def publish(self, data):
        """Publishes data to a Pub/Sub topic
        """
        future = self.publisher.publish(self.topic_path, data=data)

        if future.result():
            self.count += 1
            return True
        else:
            logging.warning('pub/sub message not published')
            return False

    def on_status(self, status):
        """Catch incoming Twitter status
        """
        tweet_json = status._json
        tweet = json.dumps(tweet_json).encode('utf-8')

        try:
            self.publish(tweet)
        except Exception as e:
            logging.exception('message')

        # Log first Tweet and restart pod when hitting total tweets
        if self.count == 1:
            logging.info('successfully published first Tweet');        
        elif self.count >= self.total_tweets:
            return False
        # Log count at LOG_COUNT interval
        if (self.count % LOG_COUNT) == 0:
            logging.info('count is: %s' % (self.count))

        return True


def main():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
        level=logging.INFO)
    logging.info('start streaming Twitter data to Pub/Sub topic');

    # Set up Twitter stream
    listener = StdOutListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESSS_TOKEN, ACCESSS_TOKEN_SECRET)
    stream = Stream(auth, listener)
    
    # Start stream with keyword filters
    stream.filter(
        track=['bigdata', 'kubernetes', 'bigquery', 'docker', 'google',
                               'googlecloud', 'golang', 'dataflow',
                              'containers', 'appengine', 'gcp', 'compute',
                               'scalability', 'gigaom', 'news', 'tech', 'apple',
                               'amazon', 'cluster', 'distributed', 'computing',
                               'cloud', 'android', 'mobile', 'ios', 'iphone',
                               'python', 'recode', 'techcrunch', 'timoreilly']
        )


if __name__ == '__main__':
    main()