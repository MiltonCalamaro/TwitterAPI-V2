import datetime as dt
import pytz
from os import environ as e

try:
    bearer_token = e['bearer_token']
except:
    bearer_token = 'your_token'
    
headers = {"Authorization": "Bearer {}".format(bearer_token)}
timezone = pytz.timezone("America/Lima")
date_now = dt.datetime.now(timezone)
start_date = dt.datetime.now(timezone).strftime("%Y-%m-%dT00:00:00Z")

params={
    'query':'', 
    'max_results':'100', 
    'start_time':start_date, 
    'expansions': 'referenced_tweets.id,author_id,in_reply_to_user_id,referenced_tweets.id.author_id,entities.mentions.username',
    'tweet.fields' : 'author_id,conversation_id,created_at,entities,id,in_reply_to_user_id,lang,public_metrics,referenced_tweets,source,text,withheld',
    'user.fields' : 'created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld'
}
