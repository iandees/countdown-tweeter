import maya
import os
import humanize
import tweepy

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_SECRET = os.environ.get('ACCESS_SECRET')
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

the_past_str = os.environ.get('PAST_DATETIME')
the_past = maya.when(the_past_str).datetime()

the_future_str = os.environ.get('FUTURE_DATETIME')
the_future = maya.when(the_future_str).datetime()

now = maya.now().datetime()

days_in = (now - the_past).days
total_days = (the_future - the_past).days

api.update_status("{} of {} days".format(
    humanize.ordinal(days_in),
    humanize.intcomma(total_days),
))
