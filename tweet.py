import maya
import os
import humanize
import tweepy
import random

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

dry_run = os.environ.get('DRY_RUN', 'true').lower() == 'true'

the_past_str = os.environ.get('PAST_DATETIME')
the_past = maya.when(the_past_str).datetime()

the_future_str = os.environ.get('FUTURE_DATETIME')
the_future = maya.when(the_future_str).datetime()

now = maya.now().datetime()

days_in = (now - the_past).days
total_days = (the_future - the_past).days

messages = [
    "{} of {} days".format(
        humanize.ordinal(days_in),
        humanize.intcomma(total_days),
    ),
    "Day {} of {}".format(
        humanize.intcomma(days_in),
        humanize.intcomma(total_days),
    ),
]

message = random.choice(messages)

if dry_run:
    logging.info("In dry run mode. Would have tweeted: %s", message)
else:
    consumer_key = os.environ.get('CONSUMER_KEY')
    consumer_secret = os.environ.get('CONSUMER_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.update_status(message)
    logging.info("Tweeted for real: %s", message)
