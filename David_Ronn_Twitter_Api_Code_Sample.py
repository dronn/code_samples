"""
This file accesses the Twitter API to get the top ten current trending hashtags
and then finds five tweets in the city of Austin with those hashtags.
Feb 2017 - David Ronn
"""
from twitter import Twitter, OAuth

# -----------------------------------------------------------------------------
# Set up authorization keys
# -----------------------------------------------------------------------------
consumer_key = 'cwSpGdQe9Jhbhwawkn7QmGCGx'
consumer_secret = 'goRaqu3WQXcuyrgI2Ce161VMb8UECE3ZxGLHcY9LBoKQpefcj3'
access_token = '830928879418277894-oTXAmo3M7eZV79uIknBajJpJIvfTOdE'
access_token_secret = 'muACL8rY80sr3l7jaI5IkxVniSa5ydUGPQs4qRbwId2Ep'

# -----------------------------------------------------------------------------
# OAuth process, using the keys and tokens
# -----------------------------------------------------------------------------
oauth = OAuth(access_token, access_token_secret, consumer_key, consumer_secret)

# -----------------------------------------------------------------------------
# Creation of the actual interface, using authentication
# -----------------------------------------------------------------------------
twitter = Twitter(auth=oauth)

# -----------------------------------------------------------------------------
# Input values here are for Austin, TX
# -----------------------------------------------------------------------------
latitude = 30.307182
longitude = -97.755996
max_range = 20
geocode =  "%f,%f,%dmi" % (latitude, longitude, max_range)
location_id = "23424977" # USA value


# ------------------------------ START FUNCTION ------------------------------ #
def getTweetsInLocation(hashtag, geocode):
    """
    Takes a hashtag and a geocode (latitude, longitude, and radius) and creates
    a list of up to five tweets for a given hashtag for that geocode location.
    """
    max_tweets = 5
    tweets_at_location = []

    # --------------------------------------------------------------------------
    # Twitter API query to find tweets for a given hashtage and location
    # Twitter API docs: https://dev.twitter.com/overview/api/tweets
    # --------------------------------------------------------------------------
    query = twitter.search.tweets(q=hashtag, geocode=geocode, count=max_tweets)

    for result in query["statuses"]:
        user = result["user"]["screen_name"]
        text = result["text"].encode('ascii', 'ignore') # Ignore emoji errors
        created_at = result["created_at"]

        user_tweet = {  'user': user, 'text': text,
                        'hashtag': hashtag, 'geocode': geocode,
                        'created_at': created_at}
        tweets_at_location.append(user_tweet)

    return tweets_at_location

# -------------------------------- END FUNCTION ------------------------------ #

# ---------------------------------------------------------------------------- #
# ----------------------------- MAIN LOGIC SECTION --------------------------- #
# ---------------------------------------------------------------------------- #

# ------------------------------------------------------------------------------
# Twitter API query to find trends for a given location using a WOEID
# (Where on Earth ID). WOEID search: http://woeid.rosselliot.co.nz/
# ------------------------------------------------------------------------------
query = twitter.trends.place(_id=location_id)

for result in query:
    top_hashtags = []
    for trend in result["trends"]:

        # ----------------------------------------------------------------------
        # Grab only hashtags, not other trends
        # ----------------------------------------------------------------------
        if trend["name"].startswith("#"):
            hashtag = trend["name"]
            top_hashtags.append(hashtag)

            # ------------------------------------------------------------------
            # Get tweets with this hashtag in a certain location
            # ------------------------------------------------------------------
            tweets = getTweetsInLocation(hashtag, geocode)

            # ------------------------------------------------------------------
            # Display output
            # ------------------------------------------------------------------
            print ("\n", hashtag)
            if not tweets:
                print ("No tweets in this location for this hashtag.")
            else:
                for tweet in tweets:
                    print ( tweet["user"], tweet["created_at"],
                            "\n", tweet["text"] )

        if len(top_hashtags) >= 10:
            break

# ---------------------------------------------------------------------------- #
# --------------------------- END MAIN LOGIC SECTION ------------------------- #
# ---------------------------------------------------------------------------- #
