import pandas as pd
import datetime as dt
from utils.get_logger import get_logger
from utils.config import timezone
logger = get_logger('tweets')
class Tweet:
    def __init__(self, dict_response):
        ### fields default
        self.tweet_id = ''
        self.created_at = ''
        self.text = ''
        self.source = ''
        self.lang = ''
        self.user_id = ''
        self.conversation_tweet_id = ''
        self.replied_user_id = ''
        ### fields public metrics
        self.retweet_count = 0
        self.reply_count = 0
        self.like_count = 0
        self.quote_count = 0
        ### fields optional entities
        self.urls_text = []
        self.mentions = {}
        self.annotations = []
        self.hashtags = []
        ### fields optional referenced_tweets
        self.retweeted_id = ''
        self.replied_tweet_id = ''
        self.quoted_tweet_id = ''
        self._get_fields_default(dict_response)
        if 'public_metrics' in dict_response:
            self._get_fields_public_metrics(dict_response['public_metrics'])
        if 'entities' in dict_response:
            self._get_fields_entities(dict_response['entities'])
        if 'referenced_tweets' in dict_response:
            self._get_fields_referenced_tweets(dict_response['referenced_tweets'])
        if not self.replied_tweet_id:
            self.replied_user_id = ''
        
        self.created_at = dt.datetime.strptime(self.created_at,'%Y-%m-%dT%H:%M:%S.%f%z')
        self.created_at = self.created_at.astimezone(timezone)


    def _get_fields_default(self, dict_response):
        self.tweet_id = dict_response['id']
        self.created_at = dict_response['created_at']
        self.text = dict_response['text']
        self.source = dict_response['source']
        self.lang = dict_response['lang']
        self.user_id = dict_response['author_id']
        self.conversation_tweet_id = dict_response['conversation_id']
        if 'in_reply_to_user_id' in dict_response:
            self.replied_user_id = dict_response['in_reply_to_user_id']
            
    def _get_fields_public_metrics(self, dict_response):
        self.retweet_count =  dict_response['retweet_count']
        self.reply_count =  dict_response['reply_count']
        self.like_count =  dict_response['like_count']
        self.quote_count =  dict_response['quote_count']
        
    def _get_fields_entities(self,dict_response):
        if 'urls' in dict_response:
            self.urls_text = [ i['expanded_url'] for i in dict_response['urls']]
        if 'mentions' in dict_response:
            self.mentions = { i['id']:i['username'] for i in dict_response['mentions']}
        if 'annotations' in dict_response:
            self.annotations = [ i['type'] for i in dict_response['annotations']]
        if 'hashtags' in dict_response:
            self.hashtags = [ i['tag'] for i in dict_response['hashtags']]
            
    def _get_fields_referenced_tweets(self, list_dict_response):
        for dict_response in list_dict_response:
            if 'retweeted' in dict_response['type']:
                self.retweeted_id = dict_response['id']
            if 'replied_to' in dict_response['type']:
                self.replied_tweet_id = dict_response['id']
            if 'quoted' in dict_response['type']:
                self.quoted_tweet_id = dict_response['id']    
                
class Tweets:
    def __init__(self, response):
        self.tweet_list = []
        self._get_response(response)
    def _get_response(self, response):
        for dict_response in response:
            tweet = Tweet(dict_response)
            self.tweet_list.append(tweet.__dict__)

class User:
    def __init__(self, dict_response):
        self.user_id = ''
        self.user_name = ''
        self.screen_name = ''
        self.description = ''
        self.location = ''
        self.verified = ''
        self.protected = ''
        self.date_joined = ''
        self.profile_image_url = ''
        self.pinned_tweet_id  = ''
        self.followers_count = 0
        self.following_count = 0
        self.tweet_count = 0
        self.listed_count = 0
        self.url_blog = ''
        self.urls_description = ''
        self.mentions_description = ''
        self.hashtags_description = ''
        self._get_fields_default(dict_response)
        if 'public_metrics' in dict_response:
            self._get_fields_public_metrics(dict_response['public_metrics'])
        if 'entities' in dict_response:
            self._get_fields_entities(dict_response['entities'])

        self.date_joined = dt.datetime.strptime(self.date_joined,'%Y-%m-%dT%H:%M:%S.%f%z')
        self.date_joined = self.date_joined.astimezone(timezone)

    def _get_fields_default(self, dict_response):
        self.user_id = dict_response['id']
        self.user_name = dict_response['name']
        self.screen_name = dict_response['username']
        self.description = dict_response['description']
        self.verified = dict_response['verified']
        self.protected = dict_response['protected']
        self.date_joined = dict_response['created_at']
        self.profile_image_url = dict_response['profile_image_url']
        if 'location' in dict_response:
            self.location = dict_response['location']
        if 'pinned_tweet_id' in dict_response:
            self.pinned_tweet_id = dict_response['pinned_tweet_id']

    def _get_fields_public_metrics(self, dict_response):
        self.followers_count = dict_response['followers_count']
        self.following_count = dict_response['following_count']
        self.tweet_count = dict_response['tweet_count']
        self.listed_count = dict_response['listed_count']

    def _get_fields_entities(self, list_dict_response):  
            if 'url' in list_dict_response:
                self.url_blog = [ i['expanded_url'] for i in list_dict_response['url']['urls']][0]
            if 'description' in list_dict_response:
                if 'urls' in list_dict_response['description']:
                    self.urls_description = [i['expanded_url'] for i in list_dict_response['description']['urls']]
                if 'mentions' in list_dict_response['description']:
                    self.mentions_description =  [i['username'] for i in list_dict_response['description']['mentions']]
                if 'hashtags' in list_dict_response['description']:
                     self.hashtags_description = [i['tag'] for i in list_dict_response['description']['hashtags']]
                            
class Users:    
    def __init__(self, response):
        self.users_list = []
        self._get_response(response)
    def _get_response(self, response):
        for dict_response in response:
            user = User(dict_response)
            self.users_list.append(user.__dict__)

def get_tweets(response):
    #### tweets en response['data']
    tweets = Tweets(response['data'])
    for i in tweets.tweet_list:
        logger.info('{} | {} | {}'.format(i['tweet_id'], i['created_at'],i['text'].replace('\n',' ')))
    df_tweets = pd.DataFrame(tweets.tweet_list)
    try:
        #### tweets en response['includes']['tweets']
        tweets = Tweets(response['includes']['tweets'])
        df_include_tweets = pd.DataFrame(tweets.tweet_list)

        ### mapear los textos completos
        dict_text = df_include_tweets.set_index('tweet_id')['text'].to_dict()
        mask = df_tweets['retweeted_id']!=''
        df_tweets.loc[mask,'text'] = df_tweets.loc[mask, 'retweeted_id'].apply(lambda x: dict_text.get(x,None))
        df_tweets = pd.concat([df_tweets, df_include_tweets])
        df_tweets = df_tweets.drop_duplicates('tweet_id')
    except:
        pass
    ### user totales incluyendo los references_tweets
    users = Users(response['includes']['users'])
    df_users = pd.DataFrame(users.users_list)
    df_tweets = pd.merge(df_tweets,df_users, how='left', on ='user_id')

    ### generar tweet_url y replied_screen_name
    df_tweets['tweet_url'] = 'https://twitter.com/'+df_tweets['screen_name']+'/status/'+df_tweets['tweet_id']
    dict_screen = df_tweets.set_index('user_id')['screen_name'].to_dict()
    dict_screen_mentions = {i:mentions[i] for mentions in df_tweets['mentions'] for i in mentions}
    dict_screen.update(dict_screen_mentions)
    df_tweets['replied_screen_name'] = df_tweets['replied_user_id'].apply(lambda x:dict_screen.get(x,''))

    return df_tweets
