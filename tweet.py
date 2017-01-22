import maya
import os
import humanize
import tweepy

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

dry_run = os.environ.get('DRY_RUN', 'true').lower() == 'true'

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.environ.get('ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

the_past_str = os.environ.get('PAST_DATETIME')
the_past = maya.when(the_past_str).datetime()

the_future_str = os.environ.get('FUTURE_DATETIME')
the_future = maya.when(the_future_str).datetime()

now = maya.now().datetime()

days_in = (now - the_past).days
total_days = (the_future - the_past).days

message = "{} of {} days".format(
    humanize.ordinal(days_in),
    humanize.intcomma(total_days),
)

if dry_run:
    logging.info("In dry run mode. Would have tweeted: %s", message)
else:
    api.update_status(message)
    logging.info("Tweeted for real: %s", message)
