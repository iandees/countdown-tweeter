# -*- coding: utf-8 -*-
import maya
import os
import humanize
import tweepy
import random
from progress_bar import progress_bar

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

dry_run = os.environ.get('DRY_RUN', 'true').lower() == 'true'

redis_previous_tweet_id_key = 'previous_tweet_id'
redis_url = os.environ.get('REDIS_URL')
previous_tweet_id = None
redis = None
if redis_url:
    import redis
    redis = redis.from_url(redis_url)
    previous_tweet_id = redis.get(redis_previous_tweet_id_key)

inauguration_2017 = maya.when("2017-01-20T12:00-05:00").datetime()
inauguration_2021 = maya.when("2021-01-20T12:00-05:00").datetime()

seconds_in_hour = (60 * 60)
seconds_in_day = (24 * seconds_in_hour)
now = maya.now().datetime()

days_in = (now - inauguration_2017).total_seconds() / seconds_in_day
days_left = (inauguration_2021 - now).total_seconds() / seconds_in_day
total_days = (inauguration_2021 - inauguration_2017).total_seconds() / seconds_in_day

messages = [
    u"Today is Election Day. Go vote!",
]

message = random.choice(messages)

if dry_run:
    logging.info("In dry run mode. Would have tweeted (in reply to %s): %s",
                 previous_tweet_id, message)
else:
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    status = api.update_status(message, in_reply_to_status_id=previous_tweet_id)
    if redis:
        redis.set(redis_previous_tweet_id_key, status.id)
    logging.info("Tweeted for real (status %s, reply to %s): %s",
                 status.id, previous_tweet_id, message)
