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
march_1 = maya.when("2020-03-01T00:00-05:00").datetime()

seconds_in_minute = 60
seconds_in_hour = (60 * seconds_in_minute)
seconds_in_day = (24 * seconds_in_hour)
now = maya.now().datetime()

seconds_in = (now - inauguration_2017).total_seconds()
total_seconds = (inauguration_2021 - inauguration_2017).total_seconds()
hours_left = (inauguration_2021 - now).total_seconds() / seconds_in_hour
minutes_left = (inauguration_2021 - now).total_seconds() / seconds_in_minute
march_day = (now - march_1).total_seconds() / seconds_in_day

if hours_left < 0:
    post_rate = 0.00
elif hours_left < 1:
    post_rate = 1.00
elif hours_left < 3:
    post_rate = 0.40
elif hours_left < 6:
    post_rate = 0.30
elif hours_left < 12:
    post_rate = 0.20
else:
    post_rate = 0.10

should_post = random.random() < post_rate

if not should_post:
    logging.info("Skipping posting because post_rate=%0.2f", post_rate)
    sys.exit(0)

messages = [
    # "Today is {}, March {}. Wear a mask, wash your hands, don't gather. Only {} of Trump left!".format(
    #     now.strftime("%A"),
    #     humanize.ordinal(round(march_day)),
    #     humanize.naturaldelta(inauguration_2021, months=False, when=now),
    # ),
    "Loading new president…\n{}\n{:0.4f}% complete.\n{} {} remaining".format(
        progress_bar(seconds_in / total_seconds, 30),
        (seconds_in / total_seconds) * 100.0,
        round(minutes_left),
        'minute' if round(minutes_left) == 1 else 'minutes',
    ),
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
