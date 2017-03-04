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

the_past_str = os.environ.get('PAST_DATETIME')
the_past = maya.when(the_past_str).datetime()

the_future_str = os.environ.get('FUTURE_DATETIME')
the_future = maya.when(the_future_str).datetime()

now = maya.now().datetime()

days_in = (now - the_past).days
days_left = (the_future - now).days
total_days = (the_future - the_past).days

messages = [
    u"Only {} days left!".format(
        humanize.intcomma(days_left),
    ),
    u"Loading…\n{}\n{:0.1f}% complete".format(
        progress_bar(float(days_in) / total_days, 36),
        (float(days_in) / total_days) * 100.0,
    )
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
    status = api.update_status(message, previous_tweet_id=previous_tweet_id)
    if redis:
        redis.set(redis_previous_tweet_id_key, status.id)
    logging.info("Tweeted for real (status %s, reply to %s): %s",
                 status.id, previous_tweet_id, message)
